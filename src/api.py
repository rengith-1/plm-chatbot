from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from .chatbot import ChatBot
from .auth import OpenBOMAuth, OpenBOMCredentials

app = FastAPI(
    title="PLM Chatbot API",
    description="An API for interacting with a PLM-aware chatbot",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize auth handler
auth_handler = OpenBOMAuth()

# Initialize chatbot
chatbot = ChatBot(auth_handler)

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None

@app.get("/")
async def root():
    """
    Serve the chat interface
    """
    return FileResponse('static/index.html')

@app.post("/auth/login")
async def login(credentials: OpenBOMCredentials):
    """Login to OpenBOM and get access token"""
    success = auth_handler.login(credentials.username, credentials.password)
    if not success:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"message": "Login successful"}

@app.post("/auth/logout")
async def logout():
    """Logout and invalidate token"""
    success = auth_handler.logout()
    if not success:
        raise HTTPException(status_code=500, detail="Logout failed")
    return {"message": "Logout successful"}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    """Send a message to the chatbot"""
    try:
        if not auth_handler.access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        response = await chatbot.handle_message(message.content)
        return ChatResponse(response=response)
    except Exception as e:
        return ChatResponse(response="", error=str(e))

@app.post("/chat/clear")
async def clear_chat():
    """Clear chat history"""
    try:
        chatbot.clear_history()
        return {"message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/boms")
async def get_boms():
    """Get list of BOMs"""
    try:
        if not auth_handler.access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        boms = chatbot.plm_client.get_boms()
        return {"boms": boms}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/catalogs")
async def get_catalogs():
    """Get list of catalogs"""
    try:
        if not auth_handler.access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        catalogs = chatbot.plm_client.get_catalogs()
        return {"catalogs": catalogs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parts/{part_number}")
async def get_part_details(part_number: str):
    """Get details for a specific part"""
    try:
        if not auth_handler.access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        details = chatbot.plm_client.get_part_details(part_number)
        if not details:
            raise HTTPException(status_code=404, detail=f"Part {part_number} not found")
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/parts/search/{query}")
async def search_parts(query: str):
    """Search for parts"""
    try:
        if not auth_handler.access_token:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        results = chatbot.plm_client.search_parts(query)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 