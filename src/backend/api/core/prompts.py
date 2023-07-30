class Prompts:
   CONTEXT_PROMPT_PREFIX = "I am traveling to {location}. Generate a 1-day itinerary for me based on the following context:\n"
   POPULAR_LOCATIONS_PROMPT = """
    Can you suggest me 3 different tourist highlights for <city> {location} </city>, which are at least 5km apart?
    Example of output (including tags):
    [
    {{location: "Singapore Zoo", fun_facts: [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}},
    {{location: "Sentosa", fun_facts: [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}}
    ]
    Please put your output in <response></response> XML tags.
    """
