import requests
from typing import Dict, Any, Optional
from config.config import PLM_API_BASE_URL, PLM_API_KEY, PLM_API_SECRET

class PLMClient:
    def __init__(self):
        self.base_url = PLM_API_BASE_URL
        self.api_key = PLM_API_KEY
        self.api_secret = PLM_API_SECRET
        self.session = requests.Session()
        self._setup_auth()

    def _setup_auth(self):
        """Set up authentication headers for API requests"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        })

    def get_part_details(self, part_number: str) -> Dict[str, Any]:
        """
        Retrieve details for a specific part number
        
        Args:
            part_number: The unique identifier for the part
            
        Returns:
            Dict containing part details
        """
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_parts(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for parts based on query and filters
        
        Args:
            query: Search query string
            filters: Optional dictionary of filters
            
        Returns:
            Dict containing search results
        """
        params = {"q": query}
        if filters:
            params.update(filters)
            
        try:
            response = self.session.get(f"{self.base_url}/parts/search", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_part_availability(self, part_number: str) -> Dict[str, Any]:
        """
        Get availability information for a specific part
        
        Args:
            part_number: The unique identifier for the part
            
        Returns:
            Dict containing availability information
        """
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}/availability")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_part_documentation(self, part_number: str) -> Dict[str, Any]:
        """
        Get documentation related to a specific part
        
        Args:
            part_number: The unique identifier for the part
            
        Returns:
            Dict containing documentation information
        """
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}/documentation")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)} 