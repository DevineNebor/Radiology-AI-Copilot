"""
Modèle pour les salles d'intervention.
"""

from sqlalchemy import Column, String, Boolean, Text
from .base import BaseModel

class Salle(BaseModel):
    """Modèle pour les salles d'intervention."""
    __tablename__ = "salles"
    
    nom = Column(String, unique=True, nullable=False)
    description = Column(Text)
    equipements = Column(Text)  # JSON string des équipements disponibles
    capacite = Column(String)  # Ex: "2 patients simultanés"
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Salle(nom='{self.nom}')>"