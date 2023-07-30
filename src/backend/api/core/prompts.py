class Prompts:
   CONTEXT_PROMPT_PREFIX = "I am traveling to {location}. Generate a 1-day itinerary for me based on the following context:\n"
   POPULAR_LOCATIONS_PROMPT = """
   Can you suggest me 3 different tourist highlights for <city> {location} </city>, which are at least 5km apart?
   Example of output (including tags):
   [
   {{"location": "Singapore Zoo", "fun_facts": [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}},
   {{"location": "Sentosa", "fun_facts": [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}}
   ]
   Please put your output in <response></response> XML tags.
   """

   ITINERARY_MAIN_PROMPT = """
   Return the location of <main_quest> {quest} </main_quest> in the following format in the following format:
   <response>
   [
      {{
         "location_name": use text inside <main_quest></main_quest> tags,
         "start_time": "13:00",
         "end_time": "16:00",
      }}
   ]
   </response>
   Delete text outside of the <response></response> tags.
   """

   ITINERARY_AFTERNOON_PROMPT = """
   Constraints:
   - I'm visiting <city_name> {city} </city_name>.  
   - Exclude <main_quest> {quest} </main_quest>.
   - Exclude locations within 5km of the following: <morning_itinerary> {morning_itinerary} </morning_itinerary>
   - Keep locations within 5km of each other.
   - The first location start_time should be 16:30 and the last location end_time should not exceed 21:00 of the same day.
   - Stay at each location for 60 minutes.
   - Leave a 30 minutes gap between locations for travel time.

   Design an itinerary around the constraints, in the following format:
   <response>
   [
      {{
         "location_name": "XXX",
         "location_address": "XXX",
         "latitude": "XXX.XXXXXXX", 
         "longtitude": "XXX.XXXXXXX",
         "start_time": "XX:XX",
         "end_time": "XX:XX",
      }}
   ], ... ,
   [
      {{
         "location_name": "XXX",
         "location_address": "XXX",
         "latitude": "XXX.XXXXXXX",
         "longtitude": "XXX.XXXXXXX",
         "start_time": "XX:XX",
         "end_time": "XX:XX",
      }}
   ]
   </response>
   Delete text outside of the <response></response> tags.
   """

   ITINERARY_MORNING_PROMPT = """
   Constraints:
   - I'm visiting <city_name> {city} </city_name>.
   - Exclude <main_quest> {quest} </main_quest>.
   - Include locations within 30 minutes of <main_quest> {quest} </main_quest>.
   - The first location start_time should be 09:00 and the last location end_time should not exceed 12:30 of the same day.
   - Stay at each location for 90 minutes.
   - Leave a 30 minutes gap between locations for travel time.
   - Keep locations within 5km of each other.

   Design an itinerary around the constraints, in the following format:
   <response>
   [
      {{
         "location_name": "XXX",
         "location_address": "XXX",
         "latitude": "XXX.XXXXXXX", 
         "longtitude": "XXX.XXXXXXX",
         "start_time": "XX:XX",
         "end_time": "XX:XX",
      }}
   ], ... ,
   [
      {{
         "location_name": "XXX",
         "location_address": "XXX",
         "latitude": "XXX.XXXXXXX",
         "longtitude": "XXX.XXXXXXX",
         "start_time": "XX:XX",
         "end_time": "XX:XX",
      }}
   ]
   </response>
   Delete text outside of the <response></response> tags.
   """
