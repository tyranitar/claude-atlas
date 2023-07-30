from typing import Any, List

import time
import asyncio

from langchain.chat_models import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from api.schemas.itinerary import ItineraryRequest
from api.schemas.quest import QuestRequest
from api.schemas.chat import ChatRequest
from api.core.prompts import Prompts

class AgentEngine:
    def __init__(self):
        self.llm = ChatAnthropic()
        self.prompts = Prompts()

    async def generate_responses(self, request: QuestRequest) -> List[str]:
        s = time.perf_counter()
        responses = await self.generate_concurrently(request=request)
        elapsed = time.perf_counter() - s
        print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")

        return responses

    async def _async_generate(self, chain: LLMChain, request: QuestRequest) -> str:
        return await chain.arun(location=request.location)

    async def generate_concurrently(self, request: QuestRequest) -> List[str]:
        prompt = self._itinerary_prompt(request=request)
        itinerary_chain = LLMChain(llm=self.llm, prompt=prompt)
        travel_chains = [itinerary_chain]

        tasks = [
            self._async_generate(chain=chain, request=request) for chain in travel_chains
        ]
        return await asyncio.gather(*tasks)

    def generate_quests(self, request: QuestRequest) -> List[str]:
        prompts = Prompts()
        template = prompts.POPULAR_LOCATIONS_PROMPT
        if request.rejected_options:
            rejected_options_str = ",".join(request.rejected_options)
            rejected_query = f"Do not include these locations, {rejected_options_str} in the suggestion."
            template += f"\n{rejected_query}"

        prompt = PromptTemplate(
            input_variables=["location"],
            template=template,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(location=request.location)

        return response

    @staticmethod
    def generate_itinerary(request: ItineraryRequest) -> PromptTemplate:
        prompts = Prompts()
        # Default: Retrieve 3 popular destinations with fun facts
        template = prompts.POPULAR_LOCATIONS_PROMPT

        if request.context:
            template = prompts.CONTEXT_PROMPT_PREFIX + request.context
        prompt = PromptTemplate(
            input_variables=["location"],
            template=template,
        )
        return prompt

    def compute_chat_response(self, request: ChatRequest) -> str:
        """
        Retrieve a list of historical chat messages and use them as context for retrieving responses.
        """
        system_message_prompt = SystemMessagePromptTemplate.from_template(
            "The following is a friendly conversation between a human and an AI. The AI is talkative and "
            "provides lots of specific details from its context. The AI will respond with plain string, replace new lines with \\n which can be easily parsed and stored into JSON, and will try to keep the responses condensed, in as few lines as possible."
        )

        message_list = []
        for message in request.messages:
            if message.role == 'user':
                message_list.append(
                    HumanMessagePromptTemplate.from_template(message.content)
                )
                input = message.content
            elif message.role == 'assistant':
                message_list.append(
                    AIMessagePromptTemplate.from_template(message.content)
                )

        # Adding SystemMessagePromptTemplate at the beginning of the message_list
        message_list.insert(0, system_message_prompt)
        message_list.insert(1, MessagesPlaceholder(variable_name="history"))
        message_list.insert(-1, HumanMessagePromptTemplate.from_template("{input}"))

        prompt = ChatPromptTemplate.from_messages(message_list)

        memory = ConversationBufferMemory(return_messages=True)
        conversation = ConversationChain(memory=memory, prompt=prompt, llm=self.llm)
        result = conversation.predict(input=input)

        return result
