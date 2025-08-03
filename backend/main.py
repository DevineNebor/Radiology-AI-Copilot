"""
Application FastAPI principale pour le service de radiologie interventionnelle.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import auth, procedures

# Création de l'instance FastAPI
app = FastAPI(
    title="Radiologie Interventionnelle SaaS",
    description="Service de gestion pour la radiologie interventionnelle",
    version="1.0.0"
)

# Configuration CORS pour permettre les requêtes depuis le frontend Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Port par défaut de Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routeurs
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(procedures.router, prefix="/api", tags=["Procedures"])

@app.get("/")
async def root():
    """Point d'entrée de l'API."""
    return {
        "message": "Bienvenue sur l'API de Radiologie Interventionnelle",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Vérification de l'état de l'API."""
    return {"status": "healthy"}