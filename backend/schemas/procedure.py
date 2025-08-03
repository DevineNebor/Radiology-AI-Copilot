"""
Schémas Pydantic pour les procédures.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcedureBase(BaseModel):
    """Schéma de base pour les procédures."""
    nom: str
    description: Optional[str] = None
    duree_moyenne: Optional[int] = None  # en minutes
    etapes: Optional[str] = None  # JSON string
    materiel_requis: Optional[str] = None  # JSON string
    precautions: Optional[str] = None

class ProcedureCreate(ProcedureBase):
    """Schéma pour la création d'une procédure."""
    pass

class ProcedureUpdate(BaseModel):
    """Schéma pour la mise à jour d'une procédure."""
    nom: Optional[str] = None
    description: Optional[str] = None
    duree_moyenne: Optional[int] = None
    etapes: Optional[str] = None
    materiel_requis: Optional[str] = None
    precautions: Optional[str] = None
    is_active: Optional[bool] = None

class ProcedureResponse(ProcedureBase):
    """Schéma de réponse pour les procédures."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True