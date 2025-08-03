"""
Composants d'authentification pour l'application Streamlit.
"""

import streamlit as st
from typing import Optional
from frontend.utils.api_client import api_client

def show_login_form():
    """Afficher le formulaire de connexion."""
    st.title("🏥 Radiologie Interventionnelle SaaS")
    st.markdown("---")
    
    # Créer des colonnes pour centrer le formulaire
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.subheader("🔐 Connexion")
        
        # Onglets pour connexion et inscription
        tab1, tab2 = st.tabs(["Connexion", "Inscription"])
        
        with tab1:
            show_login_tab()
        
        with tab2:
            show_register_tab()
        
        st.markdown("---")
        st.info("💡 **Note MVP**: Pour tester, utilisez les comptes créés lors de l'initialisation de la DB.")
        
        # Afficher les comptes de test
        with st.expander("👥 Comptes de test disponibles"):
            st.markdown("""
            | Email | Mot de passe | Rôle |
            |-------|--------------|------|
            | admin@hopital.fr | admin123 | Administrateur |
            | martin.dupont@hopital.fr | medecin123 | Médecin |
            | sophie.martin@hopital.fr | infirmier123 | Infirmier |
            | pierre.durand@hopital.fr | tech123 | Technicien |
            """)

def show_login_tab():
    """Onglet de connexion."""
    with st.form("login_form"):
        email = st.text_input(
            "📧 Email", 
            placeholder="votre.email@hopital.fr",
            help="Utilisez un des comptes de test ci-dessous"
        )
        password = st.text_input(
            "🔒 Mot de passe", 
            type="password",
            help="Mot de passe du compte test"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            login_btn = st.form_submit_button("🚀 Se connecter", use_container_width=True)
        with col2:
            if st.form_submit_button("🧪 Connexion rapide", use_container_width=True):
                # Connexion rapide avec compte test
                quick_login("martin.dupont@hopital.fr", "medecin123")
        
        if login_btn and email and password:
            perform_login(email, password)
        elif login_btn:
            st.error("⚠️ Veuillez remplir tous les champs")

def show_register_tab():
    """Onglet d'inscription."""
    with st.form("register_form"):
        st.info("📝 Créer un nouveau compte utilisateur")
        
        col1, col2 = st.columns(2)
        with col1:
            prenom = st.text_input("Prénom", placeholder="Jean")
            email = st.text_input("Email", placeholder="jean.dupont@hopital.fr")
        with col2:
            nom = st.text_input("Nom", placeholder="Dupont")
            password = st.text_input("Mot de passe", type="password")
        
        role = st.selectbox(
            "Rôle",
            options=["infirmier", "medecin", "technicien", "admin"],
            format_func=lambda x: {
                "infirmier": "👩‍⚕️ Infirmier",
                "medecin": "👨‍⚕️ Médecin", 
                "technicien": "🔧 Technicien",
                "admin": "👑 Administrateur"
            }.get(x, x)
        )
        
        if st.form_submit_button("📝 S'inscrire", use_container_width=True):
            if all([prenom, nom, email, password]):
                perform_register({
                    "prenom": prenom,
                    "nom": nom,
                    "email": email,
                    "password": password,
                    "role": role
                })
            else:
                st.error("⚠️ Veuillez remplir tous les champs")

def perform_login(email: str, password: str):
    """Effectuer la connexion."""
    with st.spinner("🔄 Connexion en cours..."):
        try:
            result = api_client.login(email, password)
            if result and "access_token" in result:
                st.session_state.user_token = result["access_token"]
                st.session_state.authenticated = True
                
                # Récupérer les infos utilisateur
                user_info = api_client.get_current_user()
                if user_info:
                    st.session_state.user_info = user_info
                    st.success(f"✅ Connexion réussie! Bienvenue {user_info.get('prenom', '')} {user_info.get('nom', '')}")
                    st.rerun()
                else:
                    st.success("✅ Connexion réussie!")
                    st.rerun()
            else:
                st.error("❌ Échec de la connexion. Vérifiez vos identifiants.")
        except Exception as e:
            st.error(f"❌ Erreur de connexion: {str(e)}")

def quick_login(email: str, password: str):
    """Connexion rapide avec compte test."""
    perform_login(email, password)

def perform_register(user_data: dict):
    """Effectuer l'inscription."""
    with st.spinner("📝 Inscription en cours..."):
        try:
            result = api_client.register(user_data)
            if result:
                st.success("✅ Inscription réussie! Vous pouvez maintenant vous connecter.")
                st.balloons()
            else:
                st.error("❌ Échec de l'inscription. L'email existe peut-être déjà.")
        except Exception as e:
            st.error(f"❌ Erreur d'inscription: {str(e)}")

def show_user_info():
    """Afficher les informations utilisateur dans la sidebar."""
    if st.session_state.get('user_info'):
        user = st.session_state.user_info
        st.markdown("**👤 Utilisateur connecté**")
        st.write(f"**{user.get('prenom', '')} {user.get('nom', '')}**")
        st.write(f"📧 {user.get('email', '')}")
        st.write(f"🏷️ {user.get('role', '').title()}")
    else:
        st.markdown("**👤 Utilisateur connecté**")
        st.write("Informations non disponibles")

def logout_user():
    """Déconnecter l'utilisateur."""
    st.session_state.authenticated = False
    st.session_state.user_token = None
    st.session_state.user_info = None
    if 'selected_intervention' in st.session_state:
        del st.session_state.selected_intervention
    st.success("👋 Déconnexion réussie!")
    st.rerun()