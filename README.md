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

# Example CURL Response
curl -d '{"location":"San Francisco"}' -H "Content-Type: application/json" -X POST http://localhost:8000/predict/
```
