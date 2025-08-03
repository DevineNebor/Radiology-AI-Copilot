"""
Schémas Pydantic pour les utilisateurs.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from backend.models.user import UserRole

class UserBase(BaseModel):
    """Schéma de base pour les utilisateurs."""
    email: EmailStr
    nom: str
    prenom: str
    role: UserRole = UserRole.INFIRMIER

class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur."""
    password: str

class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur."""
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """Schéma de réponse pour les utilisateurs."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schéma pour les tokens JWT."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Données contenues dans le token."""
    email: Optional[str] = None