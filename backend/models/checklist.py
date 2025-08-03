"""
Modèle pour les checklists de vérification.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class TypeChecklist(enum.Enum):
    """Types de checklist."""
    PRE_INTERVENTION = "pre_intervention"
    POST_INTERVENTION = "post_intervention"
    SECURITE = "securite"

class CheckList(BaseModel):
    """Modèle pour les checklists."""
    __tablename__ = "checklists"
    
    # Lien vers l'intervention
    intervention_id = Column(Integer, ForeignKey("interventions.id"), nullable=False)
    
    # Type et détails
    type_checklist = Column(Enum(TypeChecklist), nullable=False)
    nom = Column(String, nullable=False)
    
    # Items à vérifier (JSON string)
    items = Column(Text)  # Liste des items avec leur statut
    
    # Validation
    validee = Column(Boolean, default=False)
    validee_par_id = Column(Integer, ForeignKey("users.id"))
    validee_le = Column(DateTime)
    
    # Commentaires
    commentaires = Column(Text)
    
    # Relations
    intervention = relationship("Intervention")
    validee_par = relationship("User")
    
    def __repr__(self):
        return f"<CheckList(nom='{self.nom}', type='{self.type_checklist}')>"