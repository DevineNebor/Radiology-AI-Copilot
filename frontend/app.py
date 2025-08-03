"""
Application Streamlit pour le service de radiologie interventionnelle.
Interface utilisateur simplifiée pour le MVP.
"""

import streamlit as st
import requests
import json
from datetime import datetime, date
from typing import Optional

# Configuration de la page
st.set_page_config(
    page_title="Radiologie Interventionnelle SaaS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de l'API
API_BASE_URL = "http://localhost:8000"

# État de session pour l'authentification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_token" not in st.session_state:
    st.session_state.user_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

def login_user(email: str, password: str) -> bool:
    """Tenter de connecter l'utilisateur."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            st.session_state.user_token = data["access_token"]
            st.session_state.authenticated = True
            return True
        else:
            st.error("Email ou mot de passe incorrect")
            return False
    except Exception as e:
        st.error(f"Erreur de connexion à l'API: {e}")
        return False

def logout_user():
    """Déconnecter l'utilisateur."""
    st.session_state.authenticated = False
    st.session_state.user_token = None
    st.session_state.user_info = None

def get_auth_headers():
    """Récupérer les headers d'authentification."""
    if st.session_state.user_token:
        return {"Authorization": f"Bearer {st.session_state.user_token}"}
    return {}

def show_login_form():
    """Afficher le formulaire de connexion."""
    st.title("🏥 Radiologie Interventionnelle SaaS")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("Connexion")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="votre.email@hopital.fr")
            password = st.text_input("Mot de passe", type="password")
            
            if st.form_submit_button("Se connecter", use_container_width=True):
                if email and password:
                    if login_user(email, password):
                        st.success("Connexion réussie!")
                        st.rerun()
                else:
                    st.error("Veuillez remplir tous les champs")
        
        st.markdown("---")
        st.info("💡 **Note**: Cette interface est un MVP. L'authentification est simplifiée pour les tests.")

def show_main_app():
    """Afficher l'application principale."""
    # Sidebar avec informations utilisateur
    with st.sidebar:
        st.title("🏥 Radiologie SaaS")
        st.markdown("---")
        
        # Informations utilisateur (simulées)
        st.markdown("**Utilisateur connecté**")
        st.write("👤 Dr. Martin Dupont")
        st.write("📧 martin.dupont@hopital.fr")
        st.write("🏷️ Médecin")
        
        st.markdown("---")
        
        if st.button("Déconnexion", use_container_width=True):
            logout_user()
            st.rerun()
    
    # Contenu principal avec onglets
    st.title("Tableau de bord - Radiologie Interventionnelle")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📅 Planification", 
        "🔧 Procédures", 
        "💬 Feedbacks", 
        "📊 Tableau de bord"
    ])
    
    with tab1:
        show_planification_tab()
    
    with tab2:
        show_procedures_tab()
    
    with tab3:
        show_feedbacks_tab()
    
    with tab4:
        show_dashboard_tab()

def show_planification_tab():
    """Onglet de planification des interventions."""
    st.header("📅 Planification des Interventions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Interventions du jour")
        
        # Tableau simulé des interventions
        interventions_data = [
            {"Heure": "08:00", "Patient": "Patient A", "Type": "Angioplastie", "Salle": "Salle 1", "Statut": "Planifiée"},
            {"Heure": "10:30", "Patient": "Patient B", "Type": "Embolisation", "Salle": "Salle 2", "Statut": "En cours"},
            {"Heure": "14:00", "Patient": "Patient C", "Type": "Biopsie", "Salle": "Salle 1", "Statut": "Planifiée"},
        ]
        
        st.dataframe(interventions_data, use_container_width=True)
    
    with col2:
        st.subheader("Actions rapides")
        
        if st.button("➕ Nouvelle intervention", use_container_width=True):
            st.info("Fonctionnalité à implémenter")
        
        if st.button("📋 Voir planning complet", use_container_width=True):
            st.info("Fonctionnalité à implémenter")
        
        if st.button("🏥 Gestion des salles", use_container_width=True):
            st.info("Fonctionnalité à implémenter")
    
    st.markdown("---")
    st.info("💡 **MVP**: Interface simplifiée. Les données affichées sont simulées.")

def show_procedures_tab():
    """Onglet des procédures standardisées."""
    st.header("🔧 Procédures Standardisées")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Bibliothèque des procédures")
        
        # Liste simulée des procédures
        procedures = [
            {"Nom": "Angioplastie coronaire", "Durée": "90 min", "Complexité": "Élevée"},
            {"Nom": "Embolisation utérine", "Durée": "60 min", "Complexité": "Moyenne"},
            {"Nom": "Biopsie hépatique", "Durée": "30 min", "Complexité": "Faible"},
            {"Nom": "Pose de stent", "Durée": "45 min", "Complexité": "Moyenne"},
        ]
        
        for proc in procedures:
            with st.expander(f"📋 {proc['Nom']} - {proc['Durée']}"):
                st.write(f"**Durée estimée**: {proc['Durée']}")
                st.write(f"**Complexité**: {proc['Complexité']}")
                st.write("**Étapes principales**: (À définir)")
                st.write("**Matériel requis**: (À définir)")
                st.write("**Précautions**: (À définir)")
    
    with col2:
        st.subheader("Gestion")
        
        if st.button("➕ Nouvelle procédure", use_container_width=True):
            st.info("Fonctionnalité à implémenter")
        
        if st.button("✏️ Modifier procédure", use_container_width=True):
            st.info("Fonctionnalité à implémenter")
        
        if st.button("📊 Statistiques", use_container_width=True):
            st.info("Fonctionnalité à implémenter")

def show_feedbacks_tab():
    """Onglet des feedbacks post-intervention."""
    st.header("💬 Feedbacks et Retours d'Expérience")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Feedbacks récents")
        
        # Feedbacks simulés
        feedbacks = [
            {
                "Date": "2024-01-15",
                "Type": "Qualité",
                "Titre": "Excellente coordination équipe",
                "Note": "⭐⭐⭐⭐⭐",
                "Auteur": "Dr. Martin"
            },
            {
                "Date": "2024-01-14", 
                "Type": "Amélioration",
                "Titre": "Optimiser temps préparation",
                "Note": "⭐⭐⭐⭐",
                "Auteur": "Inf. Sophie"
            },
            {
                "Date": "2024-01-13",
                "Type": "Incident",
                "Titre": "Problème matériel mineur",
                "Note": "⭐⭐⭐",
                "Auteur": "Tech. Pierre"
            }
        ]
        
        for feedback in feedbacks:
            with st.expander(f"{feedback['Type']} - {feedback['Titre']} ({feedback['Date']})"):
                st.write(f"**Auteur**: {feedback['Auteur']}")
                st.write(f"**Note**: {feedback['Note']}")
                st.write("**Description**: (Détails du feedback à implémenter)")
    
    with col2:
        st.subheader("Nouveau feedback")
        
        with st.form("feedback_form"):
            intervention_id = st.selectbox(
                "Intervention", 
                ["Intervention 1", "Intervention 2", "Intervention 3"]
            )
            
            feedback_type = st.selectbox(
                "Type de feedback",
                ["Qualité", "Sécurité", "Amélioration", "Incident"]
            )
            
            titre = st.text_input("Titre")
            description = st.text_area("Description")
            note = st.slider("Note globale", 1, 5, 3)
            
            if st.form_submit_button("Envoyer feedback"):
                st.success("Feedback enregistré! (Fonctionnalité à implémenter)")

def show_dashboard_tab():
    """Onglet du tableau de bord avec métriques."""
    st.header("📊 Tableau de Bord")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Interventions aujourd'hui", "12", "2")
    
    with col2:
        st.metric("Taux de satisfaction", "4.2/5", "0.1")
    
    with col3:
        st.metric("Temps moyen", "75 min", "-5 min")
    
    with col4:
        st.metric("Salles actives", "3/4", "0")
    
    st.markdown("---")
    
    # Graphiques simulés
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Activité hebdomadaire")
        # Données simulées pour le graphique
        import pandas as pd
        import numpy as np
        
        days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        interventions = [12, 15, 18, 14, 16, 8, 5]
        
        chart_data = pd.DataFrame({
            'Jour': days,
            'Interventions': interventions
        })
        
        st.bar_chart(chart_data.set_index('Jour'))
    
    with col2:
        st.subheader("🎯 Répartition par type")
        
        types_data = pd.DataFrame({
            'Type': ['Angioplastie', 'Embolisation', 'Biopsie', 'Stent'],
            'Nombre': [35, 28, 22, 15]
        })
        
        st.bar_chart(types_data.set_index('Type'))
    
    st.markdown("---")
    st.info("💡 **MVP**: Toutes les données affichées sont simulées pour la démonstration.")

# Point d'entrée principal
def main():
    """Fonction principale de l'application."""
    if not st.session_state.authenticated:
        show_login_form()
    else:
        show_main_app()

if __name__ == "__main__":
    main()