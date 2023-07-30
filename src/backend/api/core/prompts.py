class Prompts:
   CONTEXT_PROMPT_PREFIX = "I am traveling to {location}. Generate a 1-day itinerary for me based on the following context:\n"
   POPULAR_LOCATIONS_PROMPT = """
   Suggest 3 different tourist highlights for <city> {location} </city>, which are at least 5km apart, in the following format:
   <response>
      [
         {{"location": "XXX", "fun_facts": [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}},
         {{"location": "XXX", "fun_facts": [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}},
         {{"location": "XXX", "fun_facts": [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}}
      ]
   </response>
   Delete text outside of the <response></response> tags.
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

   REGENERATE_ITINERARY_PROMPT = """
   Constraints:
   - Regenerate itinerary that is shared as an input using the above constraints, while keeping the format of the itinerary output.
   - Take care to wrap ALL outputs with <response>[{{}}, {{}}, {{}}, {{}}, {{}}]</response>. Do not include outside text.
   - Utilize user input as instructions to edit the data. Example: "Replace the 9am and 4pm locations, but keep the 730pm one." => replace the events with start_time at 9am and 4pm with brand new locations.
   - If new location added to replace an existing event has start_time before 13:00, it has to be within 30 minutes walking distance of location with start_time at 13:00 and within 15 minutes walking distance of the location preceding it.
   - If new location added to replace an existing event has start_time after 16:30, it has to be more than 5km away from all locations with start_time before 13:00 and within 15 minutes walking distance of the location preceding it.
   - Do not alter data if the user did not request a change. Keep them the same.
   ###
   Input:
   <user_input>"Replace the 11:00 and 18:00 locations"</user_input>
   [ 
   {{ "name": "Exploratorium", "start_time": "09:00", "end_time": "10:30" }},

   {{ "name": "Ferry Building Marketplace", "start_time": "11:00", "end_time": "12:30" }},

   {{ "name": "Golden Gate Park", "start_time": "13:00", "end_time": "16:00" }},

   {{ "name": "Mission Dolores Park", "start_time": "16:30", "end_time": "17:30" }},

   {{ "name": "Castro Street", "start_time": "18:00", "end_time": "19:00" }},

   {{ "name": "Corona Heights Park", "start_time": "19:30", "end_time": "20:30" }}
   ]
   Output:
   <response>
   [
   {{ "name": "Exploratorium", "start_time": "09:00", "end_time": "10:30" }},

   {{ "name": "Pier 39", "start_time": "11:00", "end_time": "12:30" }},

   {{ "name": "Golden Gate Park", "start_time": "13:00", "end_time": "16:00" }},

   {{ "name": "Mission Dolores Park", "start_time": "16:30", "end_time": "17:30" }},

   {{ "name": "The Painted Ladies", "start_time": "18:00", "end_time": "19:00" }},

   {{ "name": "Corona Heights Park", "start_time": "19:30", "end_time": "20:30" }}
   ]
   </response>

   ###
   Input:
   <user_input>"Change the Griffith Observatory location."</user_input>

   [

   {{ "name": "The Getty Center", "start_time": "10:00", "end_time": "11:00" }},

   {{ "name": "Griffith Observatory", "start_time": "11:30", "end_time": "13:00" }},

   {{ "name": "The Broad Museum", "start_time": "13:30", "end_time": "15:00" }},

   {{ "name": "Hollywood Sign", "start_time": "16:00", "end_time": "17:00" }},

   {{ "name": "Universal Studios Hollywood", "start_time": "17:30", "end_time": "19:00" }},

   {{ "name": "Santa Monica Pier", "start_time": "19:30", "end_time": "21:00" }}

   ]

   Output:
   <response>
   [
   {{ "name": "The Getty Center", "start_time": "10:00", "end_time": "11:00" }},

   {{ "name": "Los Angeles County Museum of Art", "start_time": "11:30", "end_time": "13:00" }},

   {{ "name": "The Broad Museum", "start_time": "13:30", "end_time": "15:00" }},

   {{ "name": "Hollywood Sign", "start_time": "16:00", "end_time": "17:00" }},

   {{ "name": "Universal Studios Hollywood", "start_time": "17:30", "end_time": "19:00" }},

   {{ "name": "Santa Monica Pier", "start_time": "19:30", "end_time": "21:00" }}

   ]
   </response>

   ###
   Input:
   <user_input>{input}</user_input>

   {itinerary}

   Output:
   """
