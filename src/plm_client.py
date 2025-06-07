import os
import requests
from typing import Dict, Any, Optional, List
from .auth import OpenBOMAuth

class OpenBOMClient:
    def __init__(self):
        self.base_url = "https://developer-api.openbom.com"
        self.api_key = os.getenv("OPENBOM_API_KEY")
        self.access_token = None
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """Set up session headers for OpenBOM API requests"""
        self.session.headers.update({
            **self.get_headers(),
            'Accept': 'application/json'
        })

    def refresh_session(self):
        """Refresh session headers with current auth token"""
        self._setup_session()

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with OpenBOM and get access token"""
        try:
            headers = {
                "content-type": "application/json",
                "x-openbom-appkey": self.api_key
            }
            
            data = {
                "username": username,
                "password": password
            }
            
            response = requests.post(
                f"{self.base_url}/login",
                headers=headers,
                json=data
            )
            
            if response.status_code == 200:
                self.access_token = response.json()["access_token"]
                return True
            return False
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def get_headers(self) -> dict:
        """Get headers for API requests"""
        return {
            "content-type": "application/json",
            "x-openbom-appkey": self.api_key,
            "x-openbom-accesstoken": self.access_token
        }

    def get_boms(self) -> Optional[list]:
        """Get list of BOMs"""
        try:
            response = requests.get(
                f"{self.base_url}/boms",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting BOMs: {str(e)}")
            return None

    def get_catalogs(self) -> Optional[list]:
        """Get list of catalogs"""
        try:
            response = requests.get(
                f"{self.base_url}/catalogs", 
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting catalogs: {str(e)}")
            return None

    def get_bom_details(self, bom_id: str) -> Optional[dict]:
        """Get details of a specific BOM"""
        try:
            response = requests.get(
                f"{self.base_url}/bom/{bom_id}",
                headers=self.get_headers()
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting BOM details: {str(e)}")
            return None

    def get_part_details(self, part_number: str) -> Dict[str, Any]:
        """
        Retrieve details for a specific part number from OpenBOM
        
        Args:
            part_number: The unique identifier for the part
            
        Returns:
            Dict containing part details including:
            - Basic information
            - Properties
            - BOM structure (if applicable)
        """
        try:
            # Get basic part information
            response = self.session.get(f"{self.base_url}/parts/{part_number}")
            response.raise_for_status()
            part_info = response.json()

            # Get BOM structure if available
            bom_response = self.session.get(f"{self.base_url}/parts/{part_number}/bom")
            if bom_response.status_code == 200:
                part_info['bom_structure'] = bom_response.json()

            return part_info
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def search_parts(self, query: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Search for parts in OpenBOM based on query and filters
        
        Args:
            query: Search query string
            filters: Optional dictionary of filters like:
                    - category
                    - manufacturer
                    - status
                    - custom properties
        """
        try:
            params = {
                "q": query,
                "type": "part"
            }
            if filters:
                params.update(filters)

            response = self.session.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_part_availability(self, part_number: str) -> Dict[str, Any]:
        """
        Get inventory and availability information for a part
        
        Args:
            part_number: The unique identifier for the part
        """
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}/inventory")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_part_documentation(self, part_number: str) -> Dict[str, Any]:
        """
        Get documentation and attachments related to a part
        
        Args:
            part_number: The unique identifier for the part
        """
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}/documents")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_catalog_items(self, catalog_id: str) -> List[Dict[str, Any]]:
        """Get items from a specific catalog"""
        try:
            response = self.session.get(f"{self.base_url}/catalogs/{catalog_id}/items")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return [{"error": str(e)}]

    def create_part(self, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new part in OpenBOM"""
        try:
            response = self.session.post(f"{self.base_url}/parts", json=part_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def update_part(self, part_number: str, part_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing part in OpenBOM"""
        try:
            response = self.session.put(f"{self.base_url}/parts/{part_number}", json=part_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

    def get_change_history(self, part_number: str) -> List[Dict[str, Any]]:
        """Get change history for a part"""
        try:
            response = self.session.get(f"{self.base_url}/parts/{part_number}/history")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return [{"error": str(e)}] 