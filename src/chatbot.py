from typing import List, Dict, Any
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from config.config import OPENAI_API_KEY, DEFAULT_MODEL, MAX_HISTORY_LENGTH
from .plm_client import PLMClient

class PLMChatbot:
    def __init__(self):
        self.plm_client = PLMClient()
        self.chat_model = ChatOpenAI(
            model_name=DEFAULT_MODEL,
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = """You are a helpful assistant specialized in providing information about parts from a PLM system. 
        You can search for parts, provide details about specific parts, check availability, and access documentation. 
        Always provide clear and concise information, and ask for clarification when needed."""

    def _get_part_context(self, query: str) -> str:
        """
        Get relevant part information based on the query
        """
        # First try to extract any part numbers from the query
        # This is a simple implementation - you might want to use regex or NLP for better extraction
        words = query.split()
        context = []
        
        # Search for parts related to the query
        search_results = self.plm_client.search_parts(query)
        if not isinstance(search_results, dict) or "error" not in search_results:
            context.append(f"Related parts: {str(search_results)}")

        # If we find what looks like a part number, get specific details
        for word in words:
            if any(c.isdigit() for c in word):  # Simple check for potential part numbers
                part_details = self.plm_client.get_part_details(word)
                if not isinstance(part_details, dict) or "error" not in part_details:
                    context.append(f"Part {word} details: {str(part_details)}")
                
                availability = self.plm_client.get_part_availability(word)
                if not isinstance(availability, dict) or "error" not in availability:
                    context.append(f"Part {word} availability: {str(availability)}")

        return "\n".join(context) if context else "No specific part information found."

    def process_message(self, user_message: str) -> str:
        """
        Process a user message and return a response
        """
        # Get relevant part information
        part_context = self._get_part_context(user_message)
        
        # Prepare the messages for the chat model
        messages = [
            SystemMessage(content=self.system_prompt),
            SystemMessage(content=f"Current part context:\n{part_context}")
        ]
        
        # Add conversation history
        for msg in self.conversation_history[-MAX_HISTORY_LENGTH:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # Add the current user message
        messages.append(HumanMessage(content=user_message))
        
        # Get response from the chat model
        response = self.chat_model.predict_messages(messages)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

    def clear_history(self):
        """
        Clear the conversation history
        """
        self.conversation_history = [] 