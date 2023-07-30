import langchain
from langchain.chat_models import ChatAnthropic
from langchain.cache import InMemoryCache
from langchain.chains import ConversationChain, LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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


langchain.llm_cache = InMemoryCache()

class AgentEngine:
    def __init__(self):
        self.llm = ChatAnthropic()
        self.prompts = Prompts()

    def generate_quests(self, request: QuestRequest) -> str:
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
        response = chain.run(location=request.city)

        return response

    def generate_itinerary(self, request: ItineraryRequest) -> dict:
        prompts = Prompts()
        prompt_template = PromptTemplate(input_variables=["city", "quest"], template=prompts.ITINERARY_MORNING_PROMPT)
        morning_itinerary_chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="morning_itinerary")
        prompt_template = PromptTemplate(input_variables=["quest"], template=prompts.ITINERARY_MAIN_PROMPT)
        main_quest_itinerary_chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="main_quest_itinerary")
        prompt_template = PromptTemplate(input_variables=["city", "quest", "morning_itinerary"], template=prompts.ITINERARY_AFTERNOON_PROMPT)
        afternoon_itinerary_chain = LLMChain(llm=self.llm, prompt=prompt_template, output_key="afternoon_itinerary")
        overall_chain = SequentialChain(
            chains=[morning_itinerary_chain, main_quest_itinerary_chain, afternoon_itinerary_chain],
            input_variables=["city", "quest"],
            output_variables=["morning_itinerary", "main_quest_itinerary", "afternoon_itinerary"],
        )
        response = overall_chain({"city": request.city, "quest": request.quest})

        return response

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
