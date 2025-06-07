from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
from .chatbot import PLMChatbot
from .auth import OpenBOMAuth, OpenBOMCredentials
from .plm_client import OpenBOMClient
from .chatbot import ChatBot

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

# Initialize OpenBOM client
openbom_client = OpenBOMClient()
chatbot = ChatBot(openbom_client)

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str

# Initialize auth handler
auth_handler = OpenBOMAuth()

# Dictionary to store user chatbots
user_chatbots: Dict[str, PLMChatbot] = {}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from token"""
    if not auth_handler.token or token != auth_handler.token:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    return auth_handler.user_info

@app.post("/login")
async def login(request: LoginRequest):
    """Login to OpenBOM"""
    success = openbom_client.authenticate(request.username, request.password)
    if not success:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return {"status": "success"}

@app.get("/boms")
async def get_boms():
    """Get list of BOMs"""
    if not openbom_client.access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    boms = openbom_client.get_boms()
    if not boms:
        raise HTTPException(status_code=500, detail="Failed to fetch BOMs")
    return boms

@app.get("/catalogs")
async def get_catalogs():
    """Get list of catalogs"""
    if not openbom_client.access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    catalogs = openbom_client.get_catalogs()
    if not catalogs:
        raise HTTPException(status_code=500, detail="Failed to fetch catalogs")
    return catalogs

@app.get("/bom/{bom_id}")
async def get_bom_details(bom_id: str):
    """Get details of a specific BOM"""
    if not openbom_client.access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    bom = openbom_client.get_bom_details(bom_id)
    if not bom:
        raise HTTPException(status_code=404, detail="BOM not found")
    return bom

@app.get("/")
async def root():
    """
    Serve the chat interface
    """
    return FileResponse('static/index.html')

@app.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Send a message to the chatbot and get a response
    
    Example:
        Request body: {"content": "Tell me about part ABC123"}
    """
    if not openbom_client.access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    response = await chatbot.handle_message(request.message)
    return ChatResponse(response=response)

@app.post("/clear")
async def clear_history(
    current_user: dict = Depends(get_current_user)
):
    """
    Clear the conversation history
    """
    try:
        chatbot = user_chatbots.get(auth_handler.token)
        if not chatbot:
            raise HTTPException(
                status_code=401,
                detail="Please login first"
            )
        
        chatbot.clear_history()
        return {"status": "success", "message": "Conversation history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workspaces")
async def get_workspaces(
    current_user: dict = Depends(get_current_user)
):
    """
    Get available OpenBOM workspaces
    """
    try:
        return await auth_handler.get_workspaces()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 