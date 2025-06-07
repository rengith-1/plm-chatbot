# OpenBOM PLM Chatbot

A conversational AI assistant for interacting with OpenBOM's PLM system. This chatbot helps users query and manage Bills of Materials (BOMs), catalogs, and parts information through natural language conversations.

## Features

- Natural language interface to OpenBOM
- Query BOMs and catalogs
- Search for specific parts and their details
- Authentication with OpenBOM API
- FastAPI backend with async support
- Modern web interface with real-time updates
- Secure token-based authentication
- Comprehensive logging and error handling

## Prerequisites

- Python 3.8+
- OpenBOM account
- OpenBOM API key (request from support@openbom.com)
- OpenAI API key for the chatbot functionality

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rengith-1/plm-chatbot.git
cd plm-chatbot
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
OPENBOM_API_BASE_URL=https://developer-api.openbom.com
OPENBOM_API_KEY=your_openbom_api_key
OPENAI_API_KEY=your_openai_api_key
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
LOG_LEVEL=INFO
JWT_SECRET=your-secret-key
```

## Running the Application

1. Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Start the FastAPI server:
```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

3. Open your browser and navigate to:
- Web Interface: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative API Docs: http://localhost:8000/redoc

## API Endpoints

### Authentication

- POST `/auth/login`: Login with OpenBOM credentials
- POST `/auth/refresh`: Refresh access token
- POST `/auth/logout`: Logout and invalidate token

### Chat

- POST `/chat`: Send a message to the chatbot
- GET `/chat/history`: Get conversation history
- POST `/chat/clear`: Clear conversation history

### PLM Operations

- GET `/boms`: List all BOMs
- GET `/boms/{bom_id}`: Get specific BOM details
- GET `/catalogs`: List all catalogs
- GET `/parts/search`: Search for parts

## Development

### Project Structure

```
plm_chatbot/
├── config/
│   └── config.py         # Configuration settings
├── src/
│   ├── api.py           # FastAPI application and routes
│   ├── auth.py          # Authentication handling
│   ├── chatbot.py       # Chatbot logic
│   └── plm_client.py    # OpenBOM API client
├── static/
│   ├── css/            # Stylesheets
│   ├── js/             # JavaScript files
│   └── index.html      # Web interface
├── tests/              # Test files
├── .env               # Environment variables
├── .gitignore        # Git ignore rules
└── requirements.txt   # Python dependencies
```

### Running Tests

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For OpenBOM API support, contact support@openbom.com
For issues with this chatbot, please open a GitHub issue. 