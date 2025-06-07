# PLM Chatbot

A chatbot that integrates with your PLM system to provide intelligent responses about parts and products.

## Features

- Natural language interaction with PLM system
- Part search and detailed information retrieval
- Availability checking
- Documentation access
- Conversation history management
- REST API interface

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory with the following variables:
   ```
   PLM_API_BASE_URL=your_plm_api_url
   PLM_API_KEY=your_plm_api_key
   PLM_API_SECRET=your_plm_api_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Application

1. Activate the virtual environment if not already activated
2. Run the application:
   ```bash
   python -m src.main
   ```
3. The API will be available at `http://localhost:8000`

## API Endpoints

### POST /chat
Send a message to the chatbot:
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"content": "Tell me about part ABC123"}'
```

### POST /clear
Clear the conversation history:
```bash
curl -X POST "http://localhost:8000/clear"
```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc` 