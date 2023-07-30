import requests
from bs4 import BeautifulSoup

import json

from api.schemas.quest import QuestResponse, Quest
# from api.schemas.chat import ChatResponse

class Formatter:
    @staticmethod
    def format_itinerary(response: str) -> QuestResponse:
        # getting index of substrings
        sub1 = "<response>"
        sub2 = "</response>"
        idx1 = response.index(sub1)
        idx2 = response.index(sub2)

        response = response[idx1 + len(sub1) + 1: idx2]
        resp = json.loads(response)

        # Retrieve image url and format results
        # TODO: Get better quality images
        responses = []
        for quest in resp:
            location = quest["location"]
            url = 'https://www.google.com/search?q={0}&tbm=isch'.format(location)
            content = requests.get(url).content
            soup = BeautifulSoup(content, 'lxml')
            images = soup.findAll('img')
            for image in images:
                image_url = image.get('src')
                if image_url.startswith('https'):
                    quest_url = image_url
                    break
            responses.append(
                Quest(
                    name=location,
                    fun_facts=quest["fun_facts"],
                    image_url=quest_url,
                )
            )

        formatted_response = QuestResponse(
            response=responses
        )

        return formatted_response
