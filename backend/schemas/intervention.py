"""
Schémas Pydantic pour les interventions.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.models.intervention import StatutIntervention

class InterventionBase(BaseModel):
    """Schéma de base pour les interventions."""
    patient_id: str
    patient_age: Optional[int] = None
    date_prevue: datetime
    duree_estimee: Optional[int] = None  # en minutes
    salle_id: Optional[int] = None
    medecin_id: Optional[int] = None
    type_intervention: str
    description: Optional[str] = None

class InterventionCreate(InterventionBase):
    """Schéma pour la création d'une intervention."""
    pass

class InterventionUpdate(BaseModel):
    """Schéma pour la mise à jour d'une intervention."""
    patient_age: Optional[int] = None
    date_prevue: Optional[datetime] = None
    duree_estimee: Optional[int] = None
    salle_id: Optional[int] = None
    medecin_id: Optional[int] = None
    type_intervention: Optional[str] = None
    description: Optional[str] = None
    statut: Optional[StatutIntervention] = None

class InterventionResponse(InterventionBase):
    """Schéma de réponse pour les interventions."""
    id: int
    statut: StatutIntervention
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True