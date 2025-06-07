import uvicorn
from .api import app
from .config.config import API_CONFIG

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=API_CONFIG['host'],
        port=API_CONFIG['port'],
        reload=True
    ) 