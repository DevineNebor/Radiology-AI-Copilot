"""
Application Streamlit principale pour le service de radiologie interventionnelle.
Version complète avec modules séparés et fonctionnalités avancées.
"""

import streamlit as st
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from frontend.components.auth import show_login_form, show_user_info, logout_user
from frontend.pages.interventions import show_interventions_page
from frontend.pages.procedures import show_procedures_page
from frontend.pages.feedbacks import show_feedbacks_page
from frontend.pages.dashboard import show_dashboard_page

# Configuration de la page
st.set_page_config(
    page_title="Radiologie Interventionnelle SaaS",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour améliorer l'apparence
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        border: 1px solid #e1e5e9;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        color: #155724;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        border: 1px solid #dee2e6;
        background-color: #ffffff;
        color: #495057;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: #e9ecef;
        border-color: #adb5bd;
    }
    .stSelectbox > div > div {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# État de session pour l'authentification
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_token" not in st.session_state:
    st.session_state.user_token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = None

def show_sidebar():
    """Afficher la sidebar avec navigation et informations utilisateur."""
    with st.sidebar:
        st.title("🏥 Radiologie SaaS")
        st.markdown("---")
        
        # Informations utilisateur
        show_user_info()
        
        st.markdown("---")
        
        # Navigation principale
        st.subheader("📋 Navigation")
        
        # Menu de navigation
        pages = {
            "📊 Tableau de bord": "dashboard",
            "📅 Interventions": "interventions", 
            "🔧 Procédures": "procedures",
            "💬 Feedbacks": "feedbacks"
        }
        
        # Sélection de page avec boutons radio
        selected_page = st.radio(
            "Choisir une page:",
            list(pages.keys()),
            index=0,
            key="page_selection"
        )
        
        # Stocker la page sélectionnée
        st.session_state.current_page = pages[selected_page]
        
        st.markdown("---")
        
        # Informations système
        st.subheader("ℹ️ Système")
        
        # Statut de connexion API
        if st.button("🔍 Test connexion API", use_container_width=True):
            test_api_connection()
        
        # Statistiques rapides
        with st.expander("📊 Stats rapides"):
            st.metric("Version", "1.0.0-MVP")
            st.metric("Uptime", "99.9%")
            st.metric("Utilisateurs", "4")
        
        st.markdown("---")
        
        # Bouton de déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True, type="primary"):
            logout_user()

def test_api_connection():
    """Tester la connexion à l'API."""
    try:
        from frontend.utils.api_client import api_client
        
        with st.spinner("🔄 Test de connexion..."):
            # Tenter un appel simple à l'API
            response = api_client.session.get(f"{api_client.base_url}/health")
            
            if response.status_code == 200:
                st.success("✅ API accessible")
            else:
                st.warning(f"⚠️ API répond avec le code: {response.status_code}")
                
    except Exception as e:
        st.error(f"❌ Erreur de connexion: {str(e)}")
        st.info("💡 Vérifiez que le backend est démarré avec: `uvicorn backend.main:app --reload`")

def show_main_app():
    """Afficher l'application principale avec navigation."""
    
    # Sidebar
    show_sidebar()
    
    # Contenu principal basé sur la page sélectionnée
    current_page = st.session_state.get('current_page', 'dashboard')
    
    # Header avec breadcrumb
    show_header(current_page)
    
    # Contenu de la page
    if current_page == "dashboard":
        show_dashboard_page()
    elif current_page == "interventions":
        show_interventions_page()
    elif current_page == "procedures":
        show_procedures_page()
    elif current_page == "feedbacks":
        show_feedbacks_page()
    else:
        st.error("Page non trouvée")

def show_header(current_page: str):
    """Afficher l'en-tête avec breadcrumb et actions rapides."""
    
    # Titre de la page
    page_titles = {
        "dashboard": "📊 Tableau de Bord",
        "interventions": "📅 Gestion des Interventions",
        "procedures": "🔧 Procédures Standardisées", 
        "feedbacks": "💬 Feedbacks et Retours"
    }
    
    # Breadcrumb et titre
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**🏠 Accueil** > **{page_titles.get(current_page, 'Page')}**")
    
    with col2:
        # Horloge en temps réel
        import datetime
        now = datetime.datetime.now()
        st.markdown(f"🕐 **{now.strftime('%H:%M')}** | 📅 {now.strftime('%d/%m/%Y')}")
    
    # Notifications et alertes rapides
    show_quick_alerts()

def show_quick_alerts():
    """Afficher les alertes rapides en haut de page."""
    
    # Vérifier s'il y a des alertes importantes
    alerts = get_current_alerts()
    
    if alerts:
        for alert in alerts[:2]:  # Limiter à 2 alertes max
            if alert['type'] == 'error':
                st.error(f"🚨 {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"⚠️ {alert['message']}")
            elif alert['type'] == 'info':
                st.info(f"ℹ️ {alert['message']}")

def get_current_alerts():
    """Récupérer les alertes actuelles (simulées pour le MVP)."""
    
    # Pour le MVP, on simule quelques alertes
    import random
    
    possible_alerts = [
        {"type": "info", "message": "3 nouveaux feedbacks en attente de traitement"},
        {"type": "warning", "message": "Maintenance de la salle 2 programmée demain à 14h"},
        {"type": "error", "message": "Incident signalé - Vérification requise"},
    ]
    
    # Retourner aléatoirement 0-1 alerte
    if random.random() < 0.3:  # 30% de chance d'avoir une alerte
        return [random.choice(possible_alerts)]
    
    return []

def show_welcome_message():
    """Afficher un message de bienvenue pour les nouveaux utilisateurs."""
    
    if not st.session_state.get('welcome_shown', False):
        st.balloons()
        
        with st.container():
            st.success("""
            🎉 **Bienvenue dans l'application de Radiologie Interventionnelle !**
            
            Cette interface vous permet de :
            - 📅 Gérer les interventions et plannings
            - 🔧 Consulter et créer des procédures standardisées  
            - 💬 Donner des feedbacks et suivre les améliorations
            - 📊 Visualiser les métriques et performances
            
            💡 **Astuce**: Utilisez la navigation dans la sidebar pour explorer les fonctionnalités.
            """)
        
        st.session_state.welcome_shown = True

def main():
    """Fonction principale de l'application."""
    
    # Vérifier l'authentification
    if not st.session_state.authenticated:
        show_login_form()
    else:
        # Afficher message de bienvenue si premier accès
        show_welcome_message()
        
        # Afficher l'application principale
        show_main_app()
        
        # Footer
        show_footer()

def show_footer():
    """Afficher le footer de l'application."""
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("🏥 **Radiologie Interventionnelle SaaS**")
        st.caption("Version 1.0.0 - MVP")
    
    with col2:
        st.caption("🔧 **Support technique**")
        st.caption("En cas de problème, contactez l'équipe IT")
    
    with col3:
        st.caption("📊 **Données**")
        st.caption("Dernière synchronisation: Il y a 2 min")

# Point d'entrée de l'application
if __name__ == "__main__":
    main()