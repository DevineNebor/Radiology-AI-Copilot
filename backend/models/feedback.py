"""
Modèle pour les feedbacks post-intervention.
"""

from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class TypeFeedback(enum.Enum):
    """Types de feedback."""
    QUALITE = "qualite"
    SECURITE = "securite"
    AMELIORATION = "amelioration"
    INCIDENT = "incident"

class NiveauGravite(enum.Enum):
    """Niveaux de gravité pour les incidents."""
    FAIBLE = "faible"
    MOYEN = "moyen"
    ELEVE = "eleve"
    CRITIQUE = "critique"

class Feedback(BaseModel):
    """Modèle pour les feedbacks."""
    __tablename__ = "feedbacks"
    
    # Lien vers l'intervention
    intervention_id = Column(Integer, ForeignKey("interventions.id"), nullable=False)
    
    # Auteur du feedback
    auteur_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Contenu du feedback
    type_feedback = Column(Enum(TypeFeedback), nullable=False)
    titre = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Évaluation (1-5)
    note_globale = Column(Integer)  # Note de 1 à 5
    
    # Niveau de gravité (pour les incidents)
    gravite = Column(Enum(NiveauGravite))
    
    # Actions suggérées
    actions_suggerees = Column(Text)
    
    # Relations
    intervention = relationship("Intervention")
    auteur = relationship("User")
    
    def __repr__(self):
        return f"<Feedback(titre='{self.titre}', type='{self.type_feedback}')>"