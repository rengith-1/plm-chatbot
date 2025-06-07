# This file is deprecated as authentication is now handled in plm_client.py
# Keeping this file as a placeholder in case we need to add more auth-related functionality later 

"""
Authentication module for OpenBOM PLM Chatbot.
"""

import os
from typing import Optional, Dict
import requests
from pydantic import BaseModel
from .config.config import OPENBOM_API_CONFIG

class OpenBOMCredentials(BaseModel):
    username: str
    password: str

class OpenBOMAuth:
    def __init__(self):
        self.base_url = OPENBOM_API_CONFIG['base_url']
        self.api_key = OPENBOM_API_CONFIG['api_key']
        self.access_token = None

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate with OpenBOM and get access token.
        """
        try:
            if not self.api_key:
                print("Error: OpenBOM API key not found in environment variables")
                return False

            headers = {
                "Content-Type": "application/json",
                "x-openbom-appkey": self.api_key
            }
            
            data = {
                "username": username,
                "password": password
            }
            
            # First, try the /auth/login endpoint
            response = requests.post(
                f"{self.base_url}/auth/login",
                headers=headers,
                json=data
            )
            
            # If that fails, try the /api/auth/login endpoint
            if response.status_code != 200:
                response = requests.post(
                    f"{self.base_url}/api/auth/login",
                    headers=headers,
                    json=data
                )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get("access_token") or data.get("token")
                return bool(self.access_token)
            
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return False
            
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def get_headers(self) -> Dict[str, str]:
        """
        Get headers for authenticated requests.
        """
        headers = {
            "Content-Type": "application/json",
            "x-openbom-appkey": self.api_key
        }
        if self.access_token:
            headers["x-openbom-accesstoken"] = self.access_token
            # Some APIs use Authorization header instead
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def refresh_token(self) -> bool:
        """
        Refresh the access token.
        """
        try:
            if not self.access_token:
                return False

            headers = self.get_headers()
            
            # Try both possible refresh endpoints
            for endpoint in ['/auth/refresh', '/api/auth/refresh']:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    self.access_token = data.get("access_token") or data.get("token")
                    return bool(self.access_token)
            
            return False
        except Exception as e:
            print(f"Token refresh error: {str(e)}")
            return False

    def logout(self) -> bool:
        """
        Logout and invalidate the access token.
        """
        try:
            if not self.access_token:
                return True

            headers = self.get_headers()
            
            # Try both possible logout endpoints
            for endpoint in ['/auth/logout', '/api/auth/logout']:
                response = requests.post(
                    f"{self.base_url}{endpoint}",
                    headers=headers
                )
                
                if response.status_code in [200, 204]:
                    self.access_token = None
                    return True
            
            return False
        except Exception as e:
            print(f"Logout error: {str(e)}")
            return False 