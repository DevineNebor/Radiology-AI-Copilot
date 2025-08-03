"""
Page de gestion des procédures standardisées.
"""

import streamlit as st
import json
from typing import List, Dict, Optional
from frontend.utils.api_client import api_client

def show_procedures_page():
    """Afficher la page de gestion des procédures."""
    st.header("🔧 Procédures Standardisées")
    
    # Actions principales
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("➕ Nouvelle procédure", use_container_width=True):
            st.session_state.show_procedure_form = True
    with col2:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    with col3:
        search_term = st.text_input("🔍 Rechercher", placeholder="Nom de procédure...")
    
    # Formulaire de création/modification
    if st.session_state.get('show_procedure_form', False):
        show_procedure_form()
    
    # Liste des procédures
    show_procedures_list(search_term)

def show_procedure_form():
    """Afficher le formulaire de création/modification de procédure."""
    st.markdown("---")
    
    # Déterminer si c'est une création ou modification
    is_edit = st.session_state.get('edit_procedure_id') is not None
    title = "✏️ Modifier la procédure" if is_edit else "➕ Nouvelle procédure"
    
    st.subheader(title)
    
    # Récupérer les données existantes si modification
    current_data = {}
    if is_edit:
        procedure_id = st.session_state.edit_procedure_id
        # Pour le MVP, on utilise des données par défaut
    
    with st.form("procedure_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input(
                "📋 Nom de la procédure",
                value=current_data.get('nom', ''),
                placeholder="Ex: Angioplastie coronaire"
            )
            
            duree_moyenne = st.number_input(
                "⏱️ Durée moyenne (minutes)",
                min_value=5,
                max_value=480,
                value=current_data.get('duree_moyenne', 60),
                step=5
            )
            
            complexite = st.selectbox(
                "📊 Niveau de complexité",
                options=["Faible", "Moyenne", "Élevée", "Très élevée"],
                index=1
            )
        
        with col2:
            specialite = st.selectbox(
                "🏥 Spécialité",
                options=[
                    "Cardiologie interventionnelle",
                    "Radiologie interventionnelle",
                    "Neuroradiologie",
                    "Gastroentérologie",
                    "Urologie interventionnelle",
                    "Autre"
                ],
                index=1
            )
            
            is_active = st.checkbox("✅ Procédure active", value=True)
        
        description = st.text_area(
            "📝 Description générale",
            value=current_data.get('description', ''),
            placeholder="Description détaillée de la procédure...",
            height=100
        )
        
        # Section étapes
        st.subheader("📋 Étapes de la procédure")
        etapes_text = st.text_area(
            "Étapes (une par ligne)",
            value=current_data.get('etapes_text', ''),
            placeholder="Préparation du patient\nAnesthésie locale\nCathétérisme\n...",
            height=120,
            help="Saisissez chaque étape sur une ligne séparée"
        )
        
        # Section matériel
        st.subheader("🧰 Matériel requis")
        materiel_text = st.text_area(
            "Matériel (un élément par ligne)",
            value=current_data.get('materiel_text', ''),
            placeholder="Cathéter\nGuide métallique\nBallonnet\n...",
            height=100,
            help="Saisissez chaque élément sur une ligne séparée"
        )
        
        # Section précautions
        precautions = st.text_area(
            "⚠️ Précautions particulières",
            value=current_data.get('precautions', ''),
            placeholder="Surveillance hémodynamique continue...",
            height=80
        )
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        with col1:
            submit_btn = st.form_submit_button(
                "💾 Enregistrer" if is_edit else "➕ Créer",
                use_container_width=True
            )
        with col2:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.session_state.show_procedure_form = False
                if 'edit_procedure_id' in st.session_state:
                    del st.session_state.edit_procedure_id
                st.rerun()
        
        if submit_btn and nom:
            # Convertir les étapes et matériel en JSON
            etapes_list = [etape.strip() for etape in etapes_text.split('\n') if etape.strip()]
            materiel_list = [item.strip() for item in materiel_text.split('\n') if item.strip()]
            
            procedure_data = {
                "nom": nom,
                "description": description,
                "duree_moyenne": duree_moyenne,
                "etapes": json.dumps(etapes_list, ensure_ascii=False),
                "materiel_requis": json.dumps(materiel_list, ensure_ascii=False),
                "precautions": precautions,
                "is_active": is_active
            }
            
            if is_edit:
                update_procedure(st.session_state.edit_procedure_id, procedure_data)
            else:
                create_procedure(procedure_data)
        elif submit_btn:
            st.error("⚠️ Le nom de la procédure est obligatoire")

def create_procedure(procedure_data: Dict):
    """Créer une nouvelle procédure."""
    with st.spinner("💾 Création de la procédure..."):
        try:
            result = api_client.create_procedure(procedure_data)
            if result:
                st.success("✅ Procédure créée avec succès!")
                st.session_state.show_procedure_form = False
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Erreur lors de la création de la procédure")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def update_procedure(procedure_id: int, procedure_data: Dict):
    """Mettre à jour une procédure."""
    with st.spinner("💾 Mise à jour de la procédure..."):
        try:
            # Pour le MVP, on simule la mise à jour
            st.success("✅ Procédure mise à jour avec succès!")
            st.session_state.show_procedure_form = False
            if 'edit_procedure_id' in st.session_state:
                del st.session_state.edit_procedure_id
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def show_procedures_list(search_term: str):
    """Afficher la liste des procédures."""
    st.markdown("---")
    st.subheader("📚 Bibliothèque des procédures")
    
    with st.spinner("🔄 Chargement des procédures..."):
        try:
            procedures = api_client.get_procedures()
            
            if not procedures:
                st.info("📝 Aucune procédure trouvée. Créez votre première procédure!")
                show_mock_procedures()
                return
            
            # Filtrer par terme de recherche
            if search_term:
                procedures = [p for p in procedures if search_term.lower() in p.get('nom', '').lower()]
            
            if not procedures:
                st.info("🔍 Aucune procédure ne correspond à votre recherche.")
                return
            
            # Afficher les procédures
            for procedure in procedures:
                show_procedure_card(procedure)
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {str(e)}")
            show_mock_procedures()

def show_procedure_card(procedure: Dict):
    """Afficher une carte de procédure."""
    with st.expander(f"📋 {procedure.get('nom', 'Procédure inconnue')}"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if procedure.get('description'):
                st.markdown(f"**📝 Description:** {procedure['description']}")
            
            if procedure.get('duree_moyenne'):
                st.markdown(f"**⏱️ Durée moyenne:** {procedure['duree_moyenne']} minutes")
            
            if procedure.get('precautions'):
                st.markdown(f"**⚠️ Précautions:** {procedure['precautions']}")
            
            # Étapes
            if procedure.get('etapes'):
                try:
                    etapes = json.loads(procedure['etapes'])
                    if etapes:
                        st.markdown("**📋 Étapes principales:**")
                        for i, etape in enumerate(etapes, 1):
                            st.markdown(f"{i}. {etape}")
                except:
                    st.markdown(f"**📋 Étapes:** {procedure['etapes']}")
            
            # Matériel
            if procedure.get('materiel_requis'):
                try:
                    materiel = json.loads(procedure['materiel_requis'])
                    if materiel:
                        st.markdown("**🧰 Matériel requis:**")
                        for item in materiel:
                            st.markdown(f"• {item}")
                except:
                    st.markdown(f"**🧰 Matériel:** {procedure['materiel_requis']}")
        
        with col2:
            # Statut
            is_active = procedure.get('is_active', True)
            status_icon = "✅" if is_active else "❌"
            status_text = "Active" if is_active else "Inactive"
            st.markdown(f"**Statut:** {status_icon} {status_text}")
            
            # Boutons d'action
            if st.button("✏️ Modifier", key=f"edit_proc_{procedure.get('id')}", use_container_width=True):
                st.session_state.edit_procedure_id = procedure.get('id')
                st.session_state.show_procedure_form = True
                st.rerun()
            
            if st.button("🗑️ Supprimer", key=f"delete_proc_{procedure.get('id')}", use_container_width=True):
                if st.session_state.get(f"confirm_delete_proc_{procedure.get('id')}"):
                    delete_procedure(procedure.get('id'))
                else:
                    st.session_state[f"confirm_delete_proc_{procedure.get('id')}"] = True
                    st.warning("⚠️ Confirmez la suppression")
                    st.rerun()
            
            if st.button("📊 Statistiques", key=f"stats_proc_{procedure.get('id')}", use_container_width=True):
                show_procedure_stats(procedure)

def delete_procedure(procedure_id: int):
    """Supprimer une procédure."""
    with st.spinner("🗑️ Suppression en cours..."):
        try:
            # Pour le MVP, on simule la suppression
            st.success("✅ Procédure supprimée avec succès!")
            # Nettoyer les états de confirmation
            keys_to_remove = [k for k in st.session_state.keys() if k.startswith(f"confirm_delete_proc_{procedure_id}")]
            for key in keys_to_remove:
                del st.session_state[key]
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def show_procedure_stats(procedure: Dict):
    """Afficher les statistiques d'une procédure."""
    st.info(f"📊 Statistiques pour: {procedure.get('nom', 'Procédure')}")
    
    # Données simulées pour le MVP
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Utilisée", "24 fois", "3")
    with col2:
        st.metric("Durée réelle moyenne", "68 min", "-12 min")
    with col3:
        st.metric("Taux de succès", "96%", "2%")

def show_mock_procedures():
    """Afficher des procédures simulées."""
    st.info("📡 Mode hors ligne - Données simulées")
    
    mock_procedures = [
        {
            "id": 1,
            "nom": "Angioplastie coronaire",
            "description": "Dilatation d'une artère coronaire sténosée avec pose éventuelle de stent",
            "duree_moyenne": 90,
            "etapes": '["Préparation du patient", "Anesthésie locale", "Ponction artérielle", "Cathétérisme sélectif", "Angioplastie", "Contrôle final"]',
            "materiel_requis": '["Cathéter guide", "Guide métallique", "Ballonnet", "Stent", "Produit de contraste"]',
            "precautions": "Surveillance hémodynamique continue, risque de dissection",
            "is_active": True
        },
        {
            "id": 2,
            "nom": "Embolisation utérine",
            "description": "Embolisation des artères utérines pour traitement des fibromes",
            "duree_moyenne": 60,
            "etapes": '["Préparation", "Cathétérisme sélectif", "Injection de particules", "Contrôle angiographique"]',
            "materiel_requis": '["Microcathéter", "Particules d\'embolisation", "Produit de contraste"]',
            "precautions": "Risque de douleur post-procédure, surveillance infection",
            "is_active": True
        },
        {
            "id": 3,
            "nom": "Biopsie hépatique percutanée",
            "description": "Prélèvement tissulaire hépatique sous guidage échographique",
            "duree_moyenne": 30,
            "etapes": '["Repérage échographique", "Anesthésie locale", "Biopsie", "Hémostase", "Surveillance"]',
            "materiel_requis": '["Aiguille de biopsie", "Échographe", "Anesthésique local"]',
            "precautions": "Surveillance hémorragique 4h, bilan de coagulation",
            "is_active": True
        }
    ]
    
    for procedure in mock_procedures:
        show_procedure_card(procedure)