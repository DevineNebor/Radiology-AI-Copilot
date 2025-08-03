"""
Schémas Pydantic pour les checklists.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.models.checklist import TypeChecklist

class CheckListBase(BaseModel):
    """Schéma de base pour les checklists."""
    intervention_id: int
    type_checklist: TypeChecklist
    nom: str
    items: Optional[str] = None  # JSON string
    commentaires: Optional[str] = None

class CheckListCreate(CheckListBase):
    """Schéma pour la création d'une checklist."""
    pass

class CheckListUpdate(BaseModel):
    """Schéma pour la mise à jour d'une checklist."""
    nom: Optional[str] = None
    items: Optional[str] = None
    commentaires: Optional[str] = None
    validee: Optional[bool] = None
    validee_par_id: Optional[int] = None

class CheckListResponse(CheckListBase):
    """Schéma de réponse pour les checklists."""
    id: int
    validee: bool
    validee_par_id: Optional[int] = None
    validee_le: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True