import googlemaps
import json

from api.schemas.quest import QuestResponse, Quest
from api.schemas.itinerary import ItineraryResponse, ItineraryBlock
# from api.schemas.chat import ChatResponse


BLOCK_START_TAG = "<response>"
BLOCK_END_TAG = "</response>"
MAX_WIDTH = "800"
MAX_HEIGHT = "500"
GOOGLE_API_KEY = "AIzaSyDR39HxOW9dvteOXkmHU1sgqGOjCmgj9Qc"
gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

class Formatter:
    lat_long_cache = {}
    image_cache = {}

    @staticmethod
    def format_cache_key(location: str) -> str:
        return location.replace(" ", "-").replace("'", '').replace(",", '').lower()

    @classmethod
    def format_quest(cls, city: str, response: str) -> QuestResponse:
        idx1 = response.index(BLOCK_START_TAG)
        idx2 = response.index(BLOCK_END_TAG)

        response = response[idx1 + len(BLOCK_START_TAG) + 1: idx2]
        resp = json.loads(response)

        responses = []
        for quest in resp:
            location = quest["location"]
            image_formatted_location = cls.format_cache_key(location)
            image_url = cls.image_cache.get(image_formatted_location)
            if not image_url:
                print(f"Image for {location} not found in cache...calling the GMaps API...")
                place = gmaps.places(query=f"{quest['location']}, {city}")
                photo_reference = place["results"][0]["photos"][0]["photo_reference"]
                image_url = f"""https://maps.googleapis.com/maps/api/place/photo?maxwidth={MAX_WIDTH}&maxheight={MAX_HEIGHT}&photo_reference={photo_reference}&key={GOOGLE_API_KEY}"""
                cls.image_cache[image_formatted_location] = image_url
            responses.append(
                Quest(
                    name=location,
                    fun_facts=quest["fun_facts"],
                    image_url=image_url,
                )
            )
        formatted_response = QuestResponse(
            response=responses
        )

        return formatted_response

    @classmethod
    def format_itinerary(cls, response: dict) -> ItineraryResponse:
        city = response['city']
        morning_itinerary_str = response['morning_itinerary']
        main_quest_itinerary_str = response['main_quest_itinerary']
        afternoon_itinerary_str = response['afternoon_itinerary']

        # Generate morning itinerary
        idx1 = morning_itinerary_str.index(BLOCK_START_TAG)
        idx2 = morning_itinerary_str.index(BLOCK_END_TAG)
        morning_itinerary_str = morning_itinerary_str[idx1 + len(BLOCK_START_TAG) + 1: idx2]
        morning_itinerary = json.loads(morning_itinerary_str)

        # Generate main_quest itinerary
        idx1 = main_quest_itinerary_str.index(BLOCK_START_TAG)
        idx2 = main_quest_itinerary_str.index(BLOCK_END_TAG)
        main_quest_itinerary_str = main_quest_itinerary_str[idx1 + len(BLOCK_START_TAG) + 1: idx2]
        main_quest_itinerary = json.loads(main_quest_itinerary_str)

        # Generate afternoon itinerary
        idx1 = afternoon_itinerary_str.index(BLOCK_START_TAG)
        idx2 = afternoon_itinerary_str.index(BLOCK_END_TAG)
        afternoon_itinerary_str = afternoon_itinerary_str[idx1 + len(BLOCK_START_TAG) + 1: idx2]
        afternoon_itinerary = json.loads(afternoon_itinerary_str)

        full_day_itinerary = [*morning_itinerary, *main_quest_itinerary, *afternoon_itinerary]

        itinerary_blocks = []
        for itinerary_block in full_day_itinerary:
            location_name = itinerary_block["location_name"]
            geosearch_query = f'{location_name}, {city}'
            image_formatted_location = cls.format_cache_key(geosearch_query)
            cached_value = cls.lat_long_cache.get(image_formatted_location)
            if not cached_value:
                print(f"Lat-long for {geosearch_query} not found in cache...calling the GMaps API...")
                geocode_result = gmaps.geocode(geosearch_query)
                latitude = geocode_result[0]['geometry']['location']['lat']
                longitude = geocode_result[0]['geometry']['location']['lng']
                cls.lat_long_cache[image_formatted_location] = (latitude, longitude)
            else:
                latitude = cached_value[0]
                longitude = cached_value[1]
            itinerary_blocks.append(
                ItineraryBlock(
                    name=location_name,
                    latitude=latitude,
                    longitude=longitude,
                    start_time=itinerary_block["start_time"],
                    end_time=itinerary_block["end_time"],
                )
            )
        formatted_response = ItineraryResponse(
            response=itinerary_blocks
        )

        return formatted_response
