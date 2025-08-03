"""
Modèle pour les procédures standardisées.
"""

from sqlalchemy import Column, String, Text, Boolean, Integer
from .base import BaseModel

class Procedure(BaseModel):
    """Modèle pour les procédures standardisées."""
    __tablename__ = "procedures"
    
    nom = Column(String, unique=True, nullable=False)
    description = Column(Text)
    duree_moyenne = Column(Integer)  # en minutes
    
    # Étapes de la procédure (JSON string)
    etapes = Column(Text)  # Liste des étapes au format JSON
    
    # Matériel requis (JSON string)
    materiel_requis = Column(Text)
    
    # Précautions particulières
    precautions = Column(Text)
    
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Procedure(nom='{self.nom}')>"