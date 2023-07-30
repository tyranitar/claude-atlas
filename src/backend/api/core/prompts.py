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
   <user_input>Replace the 11am and 6pm locations</user_input>
   [ 
   {{ "name": "Exploratorium", "latitude": 37.7698646, "longitude": -122.4660947, "start_time": "09:00", "end_time": "10:30" }},

   {{ "name": "Ferry Building Marketplace", "latitude": 37.770383, "longitude": -122.4701793, "start_time": "11:00", "end_time": "12:30" }},

   {{ "name": "Golden Gate Park", "latitude": 37.7694208, "longitude": -122.4862138, "start_time": "13:00", "end_time": "16:00" }},

   {{ "name": "Mission Dolores Park", "latitude": 37.80867300000001, "longitude": -122.409821, "start_time": "16:30", "end_time": "17:30" }},

   {{ "name": "Castro Street", "latitude": 37.8020074, "longitude": -122.4195532, "start_time": "18:00", "end_time": "19:00" }},

   {{ "name": "Corona Heights Park", "latitude": 37.8085771, "longitude": -122.4125282, "start_time": "19:30", "end_time": "20:30" }}
   ]
   Output:
   <response>
   [
   {{ "name": "Exploratorium", "latitude": 37.7698646, "longitude": -122.4660947, "start_time": "09:00", "end_time": "10:30" }},

   {{ "name": "Pier 39", "latitude": 37.8086731, "longitude": -122.4098211, "start_time": "11:00", "end_time": "12:30" }},

   {{ "name": "Golden Gate Park", "latitude": 37.7694208, "longitude": -122.4862138, "start_time": "13:00", "end_time": "16:00" }},

   {{ "name": "Mission Dolores Park", "latitude": 37.80867300000001, "longitude": -122.409821, "start_time": "16:30", "end_time": "17:30" }},

   {{ "name": "The Painted Ladies", "latitude": 37.7762692, "longitude": -122.4325256, "start_time": "18:00", "end_time": "19:00" }},

   {{ "name": "Corona Heights Park", "latitude": 37.8085771, "longitude": -122.4125282, "start_time": "19:30", "end_time": "20:30" }}
   ]
   </response>

   ###
   Input:
   <user_input>Change the Griffith Observatory location.</user_input>

   [

   {{ "name": "The Getty Center", "latitude": 34.0780361, "longitude": -118.4740951, "start_time": "10:00", "end_time": "11:00" }},

   {{ "name": "Griffith Observatory", "latitude": 34.1184341, "longitude": -118.3003935, "start_time": "11:30", "end_time": "13:00" }},

   {{ "name": "The Broad Museum", "latitude": 34.0543942, "longitude": -118.2505867, "start_time": "13:30", "end_time": "15:00" }},

   {{ "name": "Hollywood Sign", "latitude": 34.1341151, "longitude": -118.3215482, "start_time": "16:00", "end_time": "17:00" }},

   {{ "name": "Universal Studios Hollywood", "latitude": 34.1381178, "longitude": -118.3533783, "start_time": "17:30", "end_time": "19:00" }},

   {{ "name": "Santa Monica Pier", "latitude": 34.0103472, "longitude": -118.4962278, "start_time": "19:30", "end_time": "21:00" }}

   ]

   Output:
   <response>
   [
   {{ "name": "The Getty Center", "latitude": 34.0780361, "longitude": -118.4740951, "start_time": "10:00", "end_time": "11:00" }},

   {{ "name": "Los Angeles County Museum of Art", "latitude": 34.0639323, "longitude": -118.3592293, "start_time": "11:30", "end_time": "13:00" }},

   {{ "name": "The Broad Museum", "latitude": 34.0543942, "longitude": -118.2505867, "start_time": "13:30", "end_time": "15:00" }},

   {{ "name": "Hollywood Sign", "latitude": 34.1341151, "longitude": -118.3215482, "start_time": "16:00", "end_time": "17:00" }},

   {{ "name": "Universal Studios Hollywood", "latitude": 34.1381178, "longitude": -118.3533783, "start_time": "17:30", "end_time": "19:00" }},

   {{ "name": "Santa Monica Pier", "latitude": 34.0103472, "longitude": -118.4962278, "start_time": "19:30", "end_time": "21:00" }}

   ]
   </response>

   ###
   Input:
   <user_input>{input}</user_input>

   {itinerary}

   Output:
   """
