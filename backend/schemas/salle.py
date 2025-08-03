"""
Schémas Pydantic pour les salles.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SalleBase(BaseModel):
    """Schéma de base pour les salles."""
    nom: str
    description: Optional[str] = None
    equipements: Optional[str] = None
    capacite: Optional[str] = None

class SalleCreate(SalleBase):
    """Schéma pour la création d'une salle."""
    pass

class SalleUpdate(BaseModel):
    """Schéma pour la mise à jour d'une salle."""
    nom: Optional[str] = None
    description: Optional[str] = None
    equipements: Optional[str] = None
    capacite: Optional[str] = None
    is_active: Optional[bool] = None

class SalleResponse(SalleBase):
    """Schéma de réponse pour les salles."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True