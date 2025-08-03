"""
Routeur pour les procédures et autres endpoints de l'application.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from backend.models.base import get_db
from backend.models.user import User
from backend.routers.auth import get_current_user

router = APIRouter()

@router.get("/interventions")
async def get_interventions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des interventions."""
    # TODO: Implémenter la logique métier
    return {"message": "Liste des interventions", "user": current_user.email}

@router.get("/salles")
async def get_salles(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des salles."""
    # TODO: Implémenter la logique métier
    return {"message": "Liste des salles", "user": current_user.email}

@router.get("/procedures")
async def get_procedures(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des procédures."""
    # TODO: Implémenter la logique métier
    return {"message": "Liste des procédures", "user": current_user.email}

@router.get("/checklists")
async def get_checklists(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des checklists."""
    # TODO: Implémenter la logique métier
    return {"message": "Liste des checklists", "user": current_user.email}

@router.get("/feedbacks")
async def get_feedbacks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Récupérer la liste des feedbacks."""
    # TODO: Implémenter la logique métier
    return {"message": "Liste des feedbacks", "user": current_user.email}