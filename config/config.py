from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenBOM Configuration
PLM_API_BASE_URL = os.getenv("OPENBOM_API_URL", "https://api.openbom.com")
PLM_API_KEY = os.getenv("OPENBOM_API_KEY", "")
PLM_API_SECRET = os.getenv("OPENBOM_API_SECRET", "")

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