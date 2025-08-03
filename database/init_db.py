"""
Script d'initialisation de la base de données.
Crée toutes les tables et peut insérer des données de test.
"""

import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.base import Base, DATABASE_URL
from backend.models import User, Salle, Intervention, Procedure, CheckList, Feedback
from backend.models.user import UserRole
from backend.routers.auth import get_password_hash
from datetime import datetime, timedelta

def create_database():
    """Créer toutes les tables de la base de données."""
    print("🔧 Création des tables...")
    
    # Créer le moteur de base de données
    engine = create_engine(DATABASE_URL)
    
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Tables créées avec succès!")
    return engine

def insert_sample_data(engine):
    """Insérer des données d'exemple pour les tests."""
    print("📝 Insertion des données d'exemple...")
    
    # Créer une session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Vérifier si des données existent déjà
        if db.query(User).first():
            print("⚠️  Des données existent déjà. Suppression de l'insertion.")
            return
        
        # Créer des utilisateurs d'exemple
        users = [
            User(
                email="admin@hopital.fr",
                nom="Admin",
                prenom="Système",
                hashed_password=get_password_hash("admin123"),
                role=UserRole.ADMIN
            ),
            User(
                email="martin.dupont@hopital.fr", 
                nom="Dupont",
                prenom="Martin",
                hashed_password=get_password_hash("medecin123"),
                role=UserRole.MEDECIN
            ),
            User(
                email="sophie.martin@hopital.fr",
                nom="Martin", 
                prenom="Sophie",
                hashed_password=get_password_hash("infirmier123"),
                role=UserRole.INFIRMIER
            ),
            User(
                email="pierre.durand@hopital.fr",
                nom="Durand",
                prenom="Pierre", 
                hashed_password=get_password_hash("tech123"),
                role=UserRole.TECHNICIEN
            )
        ]
        
        for user in users:
            db.add(user)
        
        # Créer des salles d'exemple
        salles = [
            Salle(
                nom="Salle d'Angiographie 1",
                description="Salle principale équipée pour angiographie",
                equipements='{"angiographe": "Siemens Artis", "monitoring": "Philips", "defibrillateur": true}',
                capacite="1 patient"
            ),
            Salle(
                nom="Salle d'Angiographie 2", 
                description="Salle secondaire pour interventions complexes",
                equipements='{"angiographe": "GE Discovery", "monitoring": "GE", "echo": true}',
                capacite="1 patient"
            ),
            Salle(
                nom="Salle de Biopsie",
                description="Salle dédiée aux biopsies guidées",
                equipements='{"scanner": "Siemens", "table_biopsie": true, "aspiration": true}',
                capacite="1 patient"
            )
        ]
        
        for salle in salles:
            db.add(salle)
        
        # Créer des procédures d'exemple
        procedures = [
            Procedure(
                nom="Angioplastie coronaire",
                description="Dilatation d'une artère coronaire sténosée",
                duree_moyenne=90,
                etapes='["Préparation patient", "Anesthésie locale", "Ponction artérielle", "Cathétérisme", "Angioplastie", "Contrôle final"]',
                materiel_requis='["Cathéter", "Guide", "Ballonnet", "Stent", "Produit de contraste"]',
                precautions="Surveillance hémodynamique continue"
            ),
            Procedure(
                nom="Embolisation utérine",
                description="Embolisation des artères utérines pour fibromes",
                duree_moyenne=60,
                etapes='["Préparation", "Cathétérisme sélectif", "Injection particules", "Contrôle"]',
                materiel_requis='["Microcathéter", "Particules d\'embolisation", "Produit de contraste"]',
                precautions="Surveillance douleur post-procédure"
            ),
            Procedure(
                nom="Biopsie hépatique percutanée",
                description="Prélèvement tissulaire hépatique guidé",
                duree_moyenne=30,
                etapes='["Repérage échographique", "Anesthésie", "Biopsie", "Hémostase"]',
                materiel_requis='["Aiguille biopsie", "Échographe", "Anesthésique local"]',
                precautions="Surveillance hémorragique 4h"
            )
        ]
        
        for procedure in procedures:
            db.add(procedure)
        
        # Sauvegarder les changements
        db.commit()
        
        print("✅ Données d'exemple insérées avec succès!")
        print("\n👥 Utilisateurs créés:")
        print("   - admin@hopital.fr (mot de passe: admin123)")
        print("   - martin.dupont@hopital.fr (mot de passe: medecin123)")
        print("   - sophie.martin@hopital.fr (mot de passe: infirmier123)")
        print("   - pierre.durand@hopital.fr (mot de passe: tech123)")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Fonction principale d'initialisation."""
    print("🏥 Initialisation de la base de données - Radiologie Interventionnelle SaaS")
    print("=" * 70)
    
    try:
        # Créer les tables
        engine = create_database()
        
        # Demander si l'utilisateur veut insérer des données d'exemple
        response = input("\n❓ Voulez-vous insérer des données d'exemple? (y/n): ")
        if response.lower() in ['y', 'yes', 'o', 'oui']:
            insert_sample_data(engine)
        
        print("\n🎉 Initialisation terminée avec succès!")
        print("\n📋 Prochaines étapes:")
        print("   1. Démarrer le backend: uvicorn backend.main:app --reload")
        print("   2. Démarrer le frontend: streamlit run frontend/app.py")
        print("   3. Accéder à l'API: http://localhost:8000")
        print("   4. Accéder au frontend: http://localhost:8501")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        print("💡 Vérifiez que PostgreSQL est démarré et que les paramètres de connexion sont corrects.")

if __name__ == "__main__":
    main()