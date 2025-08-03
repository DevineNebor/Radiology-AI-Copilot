"""
Schémas Pydantic pour les feedbacks.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from backend.models.feedback import TypeFeedback, NiveauGravite

class FeedbackBase(BaseModel):
    """Schéma de base pour les feedbacks."""
    intervention_id: int
    type_feedback: TypeFeedback
    titre: str
    description: str
    note_globale: Optional[int] = None  # 1-5
    gravite: Optional[NiveauGravite] = None
    actions_suggerees: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    """Schéma pour la création d'un feedback."""
    pass

class FeedbackUpdate(BaseModel):
    """Schéma pour la mise à jour d'un feedback."""
    type_feedback: Optional[TypeFeedback] = None
    titre: Optional[str] = None
    description: Optional[str] = None
    note_globale: Optional[int] = None
    gravite: Optional[NiveauGravite] = None
    actions_suggerees: Optional[str] = None

class FeedbackResponse(FeedbackBase):
    """Schéma de réponse pour les feedbacks."""
    id: int
    auteur_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True