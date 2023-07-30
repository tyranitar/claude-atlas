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

from api.schemas.request_response import ItineraryRequest, ChatRequest
from api.core.prompts import Prompts

class AgentEngine:
    def __init__(self):
        self.llm = ChatAnthropic()
        self.prompts = Prompts()

    @staticmethod
    def _format_response(responses: List[str]) -> str:
        resp = responses[0]

        # getting index of substrings
        sub1 = "<response>"
        sub2 = "</response>"
        idx1 = resp.index(sub1)
        idx2 = resp.index(sub2)

        resp = resp[idx1 + len(sub1) + 1: idx2]

        return resp

    async def generate_responses(self, request: ItineraryRequest):
        s = time.perf_counter()
        responses = await self.generate_concurrently(request=request)

        if request.context:
            # TODO: Format response for frontend
            return responses[0]
        else:
            resp = self._format_response(responses)
        elapsed = time.perf_counter() - s
        print("\033[1m" + f"Concurrent executed in {elapsed:0.2f} seconds." + "\033[0m")

        return resp

    async def _async_generate(self, chain: LLMChain, request: ItineraryRequest):
        return await chain.arun(location=request.location)

    async def generate_concurrently(self, request: ItineraryRequest) -> Any:
        prompt = self._itinerary_prompt(request=request)
        itinerary_chain = LLMChain(llm=self.llm, prompt=prompt)
        travel_chains = [itinerary_chain]

        tasks = [
            self._async_generate(chain=chain, request=request) for chain in travel_chains
        ]
        return await asyncio.gather(*tasks)

    @staticmethod
    def _itinerary_prompt(request: ItineraryRequest) -> PromptTemplate:
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
