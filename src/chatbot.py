from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from .config.config import CHATBOT_CONFIG
from .plm_client import OpenBOMClient
from .auth import OpenBOMAuth
import re

class ChatBot:
    def __init__(self, auth_handler: OpenBOMAuth):
        self.auth_handler = auth_handler
        self.plm_client = OpenBOMClient(auth_handler)
        self.chat_model = ChatOpenAI(
            model_name=CHATBOT_CONFIG['model'],
            openai_api_key=CHATBOT_CONFIG['api_key'],
            temperature=CHATBOT_CONFIG['temperature']
        )
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = f"""You are a helpful assistant specialized in providing information about parts and products from OpenBOM. 
        You can:
        - Search for parts and provide detailed information
        - Check part availability and inventory
        - Access documentation and attachments
        - View and explain BOM structures
        - Access catalog information
        - Track part changes and history
        
        Always provide clear, concise information and ask for clarification when needed.
        When providing part information, include relevant details like:
        - Part number and name
        - Description and specifications
        - Current inventory status
        - BOM relationships (if applicable)
        - Recent changes or updates
        """

    def _get_part_context(self, query: str) -> str:
        """
        Get relevant part information from OpenBOM based on the query
        """
        context = []
        
        # Search for parts related to the query
        search_results = self.plm_client.search_parts(query)
        if not isinstance(search_results, dict) or "error" not in search_results:
            context.append(f"Search results: {str(search_results)}")

        # Extract potential part numbers from the query
        words = query.split()
        for word in words:
            if any(c.isdigit() for c in word):  # Simple check for potential part numbers
                # Get basic part details
                part_details = self.plm_client.get_part_details(word)
                if not isinstance(part_details, dict) or "error" not in part_details:
                    context.append(f"Part {word} details: {str(part_details)}")
                
                # Get inventory status
                availability = self.plm_client.get_part_availability(word)
                if not isinstance(availability, dict) or "error" not in availability:
                    context.append(f"Part {word} inventory: {str(availability)}")
                
                # Get documentation
                docs = self.plm_client.get_part_documentation(word)
                if not isinstance(docs, dict) or "error" not in docs:
                    context.append(f"Part {word} documentation: {str(docs)}")
                
                # Get change history
                history = self.plm_client.get_change_history(word)
                if not isinstance(history, list) or "error" not in history[0]:
                    context.append(f"Part {word} change history: {str(history)}")

        # If no specific part is found, include catalog information
        if not context:
            catalogs = self.plm_client.get_catalogs()
            if not isinstance(catalogs, list) or "error" not in catalogs[0]:
                context.append(f"Available catalogs: {str(catalogs)}")

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
            SystemMessage(content=f"Current OpenBOM context:\n{part_context}")
        ]
        
        # Add conversation history
        for msg in self.conversation_history[-CHATBOT_CONFIG['max_history_length']:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))
        
        # Add the current user message
        messages.append(HumanMessage(content=user_message))
        
        # Get response from the chat model
        response = self.chat_model.invoke(messages)
        
        # Update conversation history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response.content})
        
        return response.content

    def clear_history(self):
        """
        Clear the conversation history
        """
        self.conversation_history = []

    async def handle_message(self, message: str) -> str:
        """Process user message and return response"""
        try:
            # Check if user is asking about BOMs
            if re.search(r'boms?|bill of materials?', message.lower()):
                boms = self.plm_client.get_boms()
                if boms:
                    return self._format_bom_list(boms)
                return "I couldn't find any BOMs at the moment."
                
            # Check if user is asking about catalogs
            if re.search(r'catalogs?|parts?', message.lower()):
                catalogs = self.plm_client.get_catalogs()
                if catalogs:
                    return self._format_catalog_list(catalogs)
                return "I couldn't find any catalogs at the moment."
                
            # Check if user is asking about a specific part number
            part_match = re.search(r'part (\w+)', message.lower())
            if part_match:
                part_number = part_match.group(1)
                part_details = self.plm_client.get_part_details(part_number)
                if part_details and not part_details.get('error'):
                    return self._format_part_details(part_details)
                return f"I couldn't find details for part {part_number}."
                
            return "I can help you with information about BOMs, catalogs, and specific parts. What would you like to know?"
            
        except Exception as e:
            return f"I encountered an error: {str(e)}"
            
    def _format_bom_list(self, boms: List[Dict]) -> str:
        """Format BOM list into readable text"""
        if not boms:
            return "No BOMs found."
            
        response = "Here are the available BOMs:\n"
        for bom in boms:
            response += f"- {bom.get('name', 'Unnamed BOM')} (ID: {bom.get('id', 'N/A')})\n"
        return response
        
    def _format_catalog_list(self, catalogs: List[Dict]) -> str:
        """Format catalog list into readable text"""
        if not catalogs:
            return "No catalogs found."
            
        response = "Here are the available catalogs:\n"
        for catalog in catalogs:
            response += f"- {catalog.get('name', 'Unnamed Catalog')} (ID: {catalog.get('id', 'N/A')})\n"
        return response
        
    def _format_part_details(self, part: Dict) -> str:
        """Format part details into readable text"""
        response = f"Part Details:\n"
        for key, value in part.items():
            if key not in ['id', '_id']:
                response += f"- {key}: {value}\n"
        return response 