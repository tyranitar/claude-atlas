import os
import json
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

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from api.core.formatter import Formatter
from api.schemas.itinerary import ItineraryRequest
from api.schemas.quest import QuestRequest
from api.schemas.chat import ChatRequest
from api.schemas.gmail import SyncCalendarRequest
from api.core.prompts import Prompts


langchain.llm_cache = InMemoryCache()
# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar'
]

class AgentEngine:
    def __init__(self, formatter: Formatter):
        self.llm = ChatAnthropic(
            max_tokens_to_sample=10000,
            temperature=0
        )
        self.prompts = Prompts()
        self.formatter = formatter

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
    
    def regenerate_itinerary(self, request: ChatRequest) -> str:
        itinerary = [block.__dict__ for block in request.itinerary]
        itinerary_str = json.dumps(itinerary)
        prompts = Prompts()
        prompt = PromptTemplate(
            input_variables=["itinerary", "input"],
            template=prompts.REGENERATE_ITINERARY_PROMPT,
        )
        chain = LLMChain(llm=self.llm, prompt=prompt)
        response = chain.run(itinerary=itinerary_str, input=request.input)

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

    def sync_calendar(self, request: SyncCalendarRequest) -> bool:
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            service = build('calendar', 'v3', credentials=creds)
            for itinerary in request.events:
                lat_long = (itinerary.latitude, itinerary.longitude)
                location = ''
                for key, val in self.formatter.address_cache.items():
                    if val == lat_long:
                        location = key
                start_timestamp = f'2023-07-30T{itinerary.start_time}:00-07:00'
                end_timestamp = f'2023-07-30T{itinerary.end_time}:00-07:00'
                event = {
                    'summary': f'Visit to {itinerary.name}',
                    'location': f'{location}',
                    'start': {
                        'dateTime': start_timestamp,
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': end_timestamp,
                        'timeZone': 'America/Los_Angeles',
                    },
                    'attendees': [
                        {'email': 'terencelimxp@gmail.com'},
                        {'email': 'ken.kc.chew@gmail.com'},
                    ],
                    'reminders': {
                        'useDefault': False,
                        'overrides': [
                            {'method': 'email', 'minutes': 24 * 60},
                            {'method': 'popup', 'minutes': 10},
                        ],
                    },
                }
                event = service.events().insert(calendarId='primary', body=event).execute()
                print('Event created: %s' % (event.get('htmlLink')))
            return True
        except HttpError as error:
            print('An error occurred: %s' % error)
        return False
