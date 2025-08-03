"""
Modèle utilisateur pour l'authentification.
"""

from sqlalchemy import Column, String, Boolean, Enum
from .base import BaseModel
import enum

class UserRole(enum.Enum):
    """Rôles utilisateur dans le système."""
    ADMIN = "admin"
    MEDECIN = "medecin"
    INFIRMIER = "infirmier"
    TECHNICIEN = "technicien"

class User(BaseModel):
    """Modèle utilisateur."""
    __tablename__ = "users"
    
    email = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.INFIRMIER)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<User(email='{self.email}', nom='{self.nom}', prenom='{self.prenom}')>"