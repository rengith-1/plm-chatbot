from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from .chatbot import PLMChatbot

app = FastAPI(
    title="PLM Chatbot API",
    description="An API for interacting with a PLM-aware chatbot",
    version="1.0.0"
)

class Message(BaseModel):
    content: str

class ChatResponse(BaseModel):
    response: str
    
# Initialize the chatbot
chatbot = PLMChatbot()

@app.post("/chat", response_model=ChatResponse)
async def chat(message: Message):
    """
    Send a message to the chatbot and get a response
    """
    try:
        response = chatbot.process_message(message.content)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/clear")
async def clear_history():
    """
    Clear the conversation history
    """
    try:
        chatbot.clear_history()
        return {"status": "success", "message": "Conversation history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 