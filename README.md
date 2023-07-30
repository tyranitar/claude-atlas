# anthropic-hackathon


### Backend 

### Installation

```sh
# Create virtual environment
poetry shell

# Install dependencies
poetry install

# Export Anthropic API key
export ANTHROPIC_API_KEY=<MY_API_KEY>
```

### Starting the server

```sh
# Running the backend application
poetry run -vvv uvicorn main:app --reload

# Example CURL requests
# /quests
curl -d '{"city":"San Francisco"}' -H "Content-Type: application/json" -X POST http://localhost:8000/quests/

curl -d '{"city":"San Francisco", "rejected_options": ["Golden Gate Bridge", "Golden Gate Park"]}' -H "Content-Type: application/json" -X POST http://localhost:8000/quests/

# /itinerary
curl -d '{"city":"San Francisco", "quest": "Golden Gate Park"}' -H "Content-Type: application/json" -X POST http://localhost:8000/itinerary/

# /chat
curl -d '{"city": "San Francisco", "itinerary": [ { "name": "California Academy of Sciences", "latitude": 37.7698646, "longitude": -122.4660947, "start_time": "09:00", "end_time": "10:30", "image_url": "" }, { "name": "Japanese Tea Garden", "latitude": 37.770383, "longitude": -122.4701793, "start_time": "11:00", "end_time": "12:30", "image_url": "" }, { "name": "Golden Gate Park", "latitude": 37.7694208, "longitude": -122.4862138, "start_time": "13:00", "end_time": "16:00", "image_url": "" }, { "name": "Pier 39", "latitude": 37.80867300000001, "longitude": -122.409821, "start_time": "16:30", "end_time": "17:30", "image_url": "" }, { "name": "Lombard Street", "latitude": 37.8020074, "longitude": -122.4195532, "start_time": "18:00", "end_time": "19:00", "image_url": "" }, { "name": "Fisherman's Wharf", "latitude": 37.8085771, "longitude": -122.4125282, "start_time": "19:30", "end_time": "20:30", "image_url": "" } ],
"input": "Replace the 11am location. Replace the 430pm location. Keep all other locations."
}' -H "Content-Type: application/json" -X POST http://localhost:8000/chat/

# /sync_calendar
curl -d '{"name": "Fisherman's Wharf", "latitude": 37.8085771, "longitude": -122.4125282, "start_time": "09:00", "end_time": "10:30","image_url": ""}' -H "Content-Type: application/json" -X POST http://localhost:8000/sync_calendar/
```
