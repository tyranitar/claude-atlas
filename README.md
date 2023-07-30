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
<TODO>
```
