import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenBOM API Configuration
OPENBOM_API_CONFIG = {
    'base_url': os.getenv('OPENBOM_API_BASE_URL', 'https://developer-api.openbom.com'),
    'api_key': os.getenv('OPENBOM_API_KEY'),
    'access_token': None  # Will be set after authentication
}

# FastAPI Configuration
API_CONFIG = {
    'host': os.getenv('API_HOST', '0.0.0.0'),
    'port': int(os.getenv('API_PORT', 8000)),
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}

# Chatbot Configuration
CHATBOT_CONFIG = {
    'model': os.getenv('OPENAI_MODEL', 'gpt-4'),
    'temperature': float(os.getenv('OPENAI_TEMPERATURE', 0.7)),
    'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', 150)),
    'api_key': os.getenv('OPENAI_API_KEY')
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('LOG_FILE', 'plm_chatbot.log')
}

# Security Configuration
SECURITY_CONFIG = {
    'jwt_secret': os.getenv('JWT_SECRET', 'your-secret-key'),
    'jwt_algorithm': 'HS256',
    'jwt_expiration': int(os.getenv('JWT_EXPIRATION', 3600))  # 1 hour
}

# OpenBOM Workspace Settings
OPENBOM_WORKSPACE_ID = os.getenv("OPENBOM_WORKSPACE_ID", "")
OPENBOM_COMPANY_ID = os.getenv("OPENBOM_COMPANY_ID", "")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Chat Configuration
MAX_HISTORY_LENGTH = 10
DEFAULT_MODEL = "gpt-4-turbo-preview"

# API Rate Limiting
MAX_REQUESTS_PER_MINUTE = 60
RATE_LIMIT_ENABLED = True 