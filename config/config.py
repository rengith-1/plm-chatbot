from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# PLM System Configuration
PLM_API_BASE_URL = os.getenv("PLM_API_BASE_URL", "")
PLM_API_KEY = os.getenv("PLM_API_KEY", "")
PLM_API_SECRET = os.getenv("PLM_API_SECRET", "")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Chat Configuration
MAX_HISTORY_LENGTH = 10
DEFAULT_MODEL = "gpt-4-turbo-preview" 