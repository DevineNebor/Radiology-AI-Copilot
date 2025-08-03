"""
Client API centralisé pour les interactions avec le backend FastAPI.
"""

import requests
import streamlit as st
from typing import Dict, List, Optional, Any
import json

class APIClient:
    """Client pour interagir avec l'API FastAPI."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _get_headers(self) -> Dict[str, str]:
        """Récupérer les headers avec token d'authentification."""
        headers = {"Content-Type": "application/json"}
        if hasattr(st.session_state, 'user_token') and st.session_state.user_token:
            headers["Authorization"] = f"Bearer {st.session_state.user_token}"
        return headers
    
    def _handle_response(self, response: requests.Response) -> Optional[Dict]:
        """Gérer la réponse de l'API."""
        try:
            if response.status_code == 401:
                st.error("Session expirée. Veuillez vous reconnecter.")
                st.session_state.authenticated = False
                st.session_state.user_token = None
                return None
            
            if response.status_code >= 400:
                error_detail = response.json().get("detail", "Erreur inconnue")
                st.error(f"Erreur API: {error_detail}")
                return None
            
            return response.json() if response.content else {}
        except Exception as e:
            st.error(f"Erreur de communication: {str(e)}")
            return None
    
    # Authentification
    def login(self, email: str, password: str) -> Optional[Dict]:
        """Connexion utilisateur."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json={"email": email, "password": password}
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur de connexion: {str(e)}")
            return None
    
    def register(self, user_data: Dict) -> Optional[Dict]:
        """Inscription utilisateur."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=user_data
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur d'inscription: {str(e)}")
            return None
    
    def get_current_user(self) -> Optional[Dict]:
        """Récupérer les informations de l'utilisateur connecté."""
        try:
            response = self.session.get(
                f"{self.base_url}/auth/me",
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur récupération utilisateur: {str(e)}")
            return None
    
    # Interventions
    def get_interventions(self) -> Optional[List[Dict]]:
        """Récupérer la liste des interventions."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/interventions",
                headers=self._get_headers()
            )
            result = self._handle_response(response)
            return result if isinstance(result, list) else []
        except Exception as e:
            st.error(f"Erreur récupération interventions: {str(e)}")
            return []
    
    def create_intervention(self, intervention_data: Dict) -> Optional[Dict]:
        """Créer une nouvelle intervention."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/interventions",
                json=intervention_data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur création intervention: {str(e)}")
            return None
    
    def update_intervention(self, intervention_id: int, data: Dict) -> Optional[Dict]:
        """Mettre à jour une intervention."""
        try:
            response = self.session.put(
                f"{self.base_url}/api/interventions/{intervention_id}",
                json=data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur mise à jour intervention: {str(e)}")
            return None
    
    def delete_intervention(self, intervention_id: int) -> bool:
        """Supprimer une intervention."""
        try:
            response = self.session.delete(
                f"{self.base_url}/api/interventions/{intervention_id}",
                headers=self._get_headers()
            )
            return response.status_code == 200
        except Exception as e:
            st.error(f"Erreur suppression intervention: {str(e)}")
            return False
    
    # Salles
    def get_salles(self) -> Optional[List[Dict]]:
        """Récupérer la liste des salles."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/salles",
                headers=self._get_headers()
            )
            result = self._handle_response(response)
            return result if isinstance(result, list) else []
        except Exception as e:
            st.error(f"Erreur récupération salles: {str(e)}")
            return []
    
    def create_salle(self, salle_data: Dict) -> Optional[Dict]:
        """Créer une nouvelle salle."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/salles",
                json=salle_data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur création salle: {str(e)}")
            return None
    
    # Procédures
    def get_procedures(self) -> Optional[List[Dict]]:
        """Récupérer la liste des procédures."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/procedures",
                headers=self._get_headers()
            )
            result = self._handle_response(response)
            return result if isinstance(result, list) else []
        except Exception as e:
            st.error(f"Erreur récupération procédures: {str(e)}")
            return []
    
    def create_procedure(self, procedure_data: Dict) -> Optional[Dict]:
        """Créer une nouvelle procédure."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/procedures",
                json=procedure_data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur création procédure: {str(e)}")
            return None
    
    # Feedbacks
    def get_feedbacks(self) -> Optional[List[Dict]]:
        """Récupérer la liste des feedbacks."""
        try:
            response = self.session.get(
                f"{self.base_url}/api/feedbacks",
                headers=self._get_headers()
            )
            result = self._handle_response(response)
            return result if isinstance(result, list) else []
        except Exception as e:
            st.error(f"Erreur récupération feedbacks: {str(e)}")
            return []
    
    def create_feedback(self, feedback_data: Dict) -> Optional[Dict]:
        """Créer un nouveau feedback."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/feedbacks",
                json=feedback_data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur création feedback: {str(e)}")
            return None
    
    # Checklists
    def get_checklists(self, intervention_id: Optional[int] = None) -> Optional[List[Dict]]:
        """Récupérer la liste des checklists."""
        try:
            url = f"{self.base_url}/api/checklists"
            if intervention_id:
                url += f"?intervention_id={intervention_id}"
            
            response = self.session.get(url, headers=self._get_headers())
            result = self._handle_response(response)
            return result if isinstance(result, list) else []
        except Exception as e:
            st.error(f"Erreur récupération checklists: {str(e)}")
            return []
    
    def create_checklist(self, checklist_data: Dict) -> Optional[Dict]:
        """Créer une nouvelle checklist."""
        try:
            response = self.session.post(
                f"{self.base_url}/api/checklists",
                json=checklist_data,
                headers=self._get_headers()
            )
            return self._handle_response(response)
        except Exception as e:
            st.error(f"Erreur création checklist: {str(e)}")
            return None

# Instance globale du client API
api_client = APIClient()