-- Main Quest Brainstorm Prompt


<prompt>
"""
Suggest 3 different tourist highlights for <city> {location} </city>, which are at least 5km apart, in the following format:
    [
        {{location: "Singapore Zoo", fun_facts: [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}},
        {{location: "Sentosa", fun_facts: [<fun_fact_1>, <fun_fact_2>, <fun_fact_3>]}}
    ]

Put your output in <response></response> XML tags.
"""
</prompt>

-- Example output:
 [
    {
        'location': "Gardens by the Bay",
        'fun_facts': ["It has 2 huge domed conservatories, the Flower Dome and the Cloud Forest, hosting plants from Mediterranean and tropic climates.", 
                      "The Supertree Grove has 18 towering tree-like structures up to 16 stories tall, covered in plants and lit up at night.",
                      "It hosts spectacular light shows using music, lighting, and projections on the Supertrees regularly at night."],
    },
    
    {
        'location': "Sentosa Island",
        'fun_facts': ["It has pristine beaches, resorts, theme parks like Universal Studios, and historical sites like Fort Siloso.",
                      "It's home to SEA Aquarium, one of the world's largest aquariums with 100,000 marine animals.",
                      "You can visit via cable car, walking, or road for a fun day trip from mainland Singapore."],
    },
    
    {
        'location': "Singapore Zoo", 
        'fun_facts': ["It exhibits over 2,800 animals representing over 300 species including polar bears and lemurs.",
                      "It has open concept enclosures separated from visitors by moats or glass.",
                      "The zoo offers unique shows like the elephant presentation and orangutan feeding time."],
    },
    {
        'location': "Marina Bay Sands",
        'fun_facts': ["It has a unique infinity pool on the 57th floor with incredible views of the city skyline.",
                      "The ArtScience Museum is shaped like a lotus flower and hosts international exhibits.", 
                      "There are celebrity chef restaurants, a mall, casino, and the iconic Marina Bay Sands hotel."],
    },

    {
        'location': "Little India",
        'fun_facts': ["It's one of Singapore's most vibrant ethnic districts known for shopping, dining, and culture.",
                      "Mustafa Centre is a famous 24-hour department store stocking everything.",
                      "The Sri Veeramakaliamman Temple has colorful sculptures of Hindu deities."],
    },

    {
        'location': "Chinatown",
        'fun_facts': ["It has historic shophouses, Chinese temples, and small alleys to explore like Trengganu Street.",
                      "There are bustling markets selling souvenirs, spices, and street food.",
                      "At Buddha Tooth Relic Temple - one of the largest Buddhist temples in Singapore."],  
    }
]