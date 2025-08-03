"""
Modèle pour les interventions planifiées.
"""

from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship
from .base import BaseModel
import enum

class StatutIntervention(enum.Enum):
    """Statuts possibles d'une intervention."""
    PLANIFIEE = "planifiee"
    EN_COURS = "en_cours"
    TERMINEE = "terminee"
    ANNULEE = "annulee"

class Intervention(BaseModel):
    """Modèle pour les interventions."""
    __tablename__ = "interventions"
    
    # Informations patient (anonymisées pour le MVP)
    patient_id = Column(String, nullable=False)  # ID anonyme
    patient_age = Column(Integer)
    
    # Planification
    date_prevue = Column(DateTime, nullable=False)
    duree_estimee = Column(Integer)  # en minutes
    
    # Liens vers autres entités
    salle_id = Column(Integer, ForeignKey("salles.id"))
    medecin_id = Column(Integer, ForeignKey("users.id"))
    
    # Détails intervention
    type_intervention = Column(String, nullable=False)
    description = Column(Text)
    statut = Column(Enum(StatutIntervention), default=StatutIntervention.PLANIFIEE)
    
    # Relations
    salle = relationship("Salle")
    medecin = relationship("User")
    
    def __repr__(self):
        return f"<Intervention(patient_id='{self.patient_id}', type='{self.type_intervention}')>"