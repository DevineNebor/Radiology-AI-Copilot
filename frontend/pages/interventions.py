"""
Page de gestion des interventions - CRUD complet.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, time
from typing import List, Dict, Optional
from frontend.utils.api_client import api_client

def show_interventions_page():
    """Afficher la page de gestion des interventions."""
    st.header("📅 Gestion des Interventions")
    
    # Actions principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Nouvelle intervention", use_container_width=True):
            st.session_state.show_intervention_form = True
    with col2:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    with col3:
        filter_status = st.selectbox(
            "Filtrer par statut",
            ["Tous", "planifiee", "en_cours", "terminee", "annulee"],
            format_func=lambda x: {
                "Tous": "📋 Tous",
                "planifiee": "⏳ Planifiée",
                "en_cours": "🔄 En cours",
                "terminee": "✅ Terminée",
                "annulee": "❌ Annulée"
            }.get(x, x)
        )
    with col4:
        show_today_only = st.checkbox("📅 Aujourd'hui seulement")
    
    # Formulaire de création/modification
    if st.session_state.get('show_intervention_form', False):
        show_intervention_form()
    
    # Liste des interventions
    show_interventions_list(filter_status, show_today_only)

def show_intervention_form():
    """Afficher le formulaire de création/modification d'intervention."""
    st.markdown("---")
    
    # Déterminer si c'est une création ou modification
    is_edit = st.session_state.get('edit_intervention_id') is not None
    title = "✏️ Modifier l'intervention" if is_edit else "➕ Nouvelle intervention"
    
    st.subheader(title)
    
    # Récupérer les données existantes si modification
    current_data = {}
    if is_edit:
        intervention_id = st.session_state.edit_intervention_id
        # Ici on devrait récupérer les données de l'intervention
        # Pour le MVP, on utilise des données par défaut
    
    with st.form("intervention_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_id = st.text_input(
                "🏥 ID Patient (anonyme)",
                value=current_data.get('patient_id', ''),
                placeholder="PAT-2024-001"
            )
            
            patient_age = st.number_input(
                "👤 Âge du patient",
                min_value=0,
                max_value=120,
                value=current_data.get('patient_age', 65),
                step=1
            )
            
            type_intervention = st.selectbox(
                "🔧 Type d'intervention",
                options=[
                    "Angioplastie coronaire",
                    "Embolisation utérine", 
                    "Biopsie hépatique",
                    "Pose de stent",
                    "Thrombectomie",
                    "Drainage percutané",
                    "Autre"
                ],
                index=0
            )
            
            if type_intervention == "Autre":
                type_intervention = st.text_input("Préciser le type d'intervention")
        
        with col2:
            date_intervention = st.date_input(
                "📅 Date prévue",
                value=current_data.get('date_prevue', date.today()),
                min_value=date.today()
            )
            
            heure_intervention = st.time_input(
                "🕐 Heure prévue",
                value=current_data.get('heure_prevue', time(8, 0))
            )
            
            duree_estimee = st.number_input(
                "⏱️ Durée estimée (minutes)",
                min_value=15,
                max_value=480,
                value=current_data.get('duree_estimee', 90),
                step=15
            )
            
            # Récupérer les salles disponibles
            salles = get_salles_options()
            salle_id = st.selectbox(
                "🏥 Salle d'intervention",
                options=list(salles.keys()),
                format_func=lambda x: salles.get(x, "Salle inconnue")
            )
        
        description = st.text_area(
            "📝 Description / Notes",
            value=current_data.get('description', ''),
            placeholder="Détails spécifiques de l'intervention..."
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
                st.session_state.show_intervention_form = False
                if 'edit_intervention_id' in st.session_state:
                    del st.session_state.edit_intervention_id
                st.rerun()
        
        if submit_btn:
            # Combiner date et heure
            datetime_prevue = datetime.combine(date_intervention, heure_intervention)
            
            intervention_data = {
                "patient_id": patient_id,
                "patient_age": patient_age,
                "date_prevue": datetime_prevue.isoformat(),
                "duree_estimee": duree_estimee,
                "salle_id": salle_id if salle_id != "none" else None,
                "type_intervention": type_intervention,
                "description": description
            }
            
            if is_edit:
                update_intervention(st.session_state.edit_intervention_id, intervention_data)
            else:
                create_intervention(intervention_data)

def get_salles_options() -> Dict[str, str]:
    """Récupérer les options de salles disponibles."""
    try:
        salles = api_client.get_salles()
        if salles:
            options = {str(salle['id']): f"🏥 {salle['nom']}" for salle in salles}
            options["none"] = "❓ Non assignée"
            return options
        else:
            return {"none": "❓ Aucune salle disponible"}
    except:
        return {"none": "❌ Erreur chargement salles"}

def create_intervention(intervention_data: Dict):
    """Créer une nouvelle intervention."""
    with st.spinner("💾 Création de l'intervention..."):
        try:
            result = api_client.create_intervention(intervention_data)
            if result:
                st.success("✅ Intervention créée avec succès!")
                st.session_state.show_intervention_form = False
                st.balloons()
                st.rerun()
            else:
                st.error("❌ Erreur lors de la création de l'intervention")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def update_intervention(intervention_id: int, intervention_data: Dict):
    """Mettre à jour une intervention."""
    with st.spinner("💾 Mise à jour de l'intervention..."):
        try:
            result = api_client.update_intervention(intervention_id, intervention_data)
            if result:
                st.success("✅ Intervention mise à jour avec succès!")
                st.session_state.show_intervention_form = False
                if 'edit_intervention_id' in st.session_state:
                    del st.session_state.edit_intervention_id
                st.rerun()
            else:
                st.error("❌ Erreur lors de la mise à jour")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def show_interventions_list(filter_status: str, show_today_only: bool):
    """Afficher la liste des interventions."""
    st.markdown("---")
    st.subheader("📋 Liste des interventions")
    
    with st.spinner("🔄 Chargement des interventions..."):
        try:
            interventions = api_client.get_interventions()
            
            if not interventions:
                st.info("📝 Aucune intervention trouvée. Créez votre première intervention!")
                return
            
            # Filtrer les interventions
            filtered_interventions = filter_interventions(
                interventions, filter_status, show_today_only
            )
            
            if not filtered_interventions:
                st.info("🔍 Aucune intervention ne correspond aux filtres sélectionnés.")
                return
            
            # Afficher les interventions sous forme de cartes
            for intervention in filtered_interventions:
                show_intervention_card(intervention)
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {str(e)}")
            # Afficher des données simulées en cas d'erreur API
            show_mock_interventions()

def filter_interventions(interventions: List[Dict], status_filter: str, today_only: bool) -> List[Dict]:
    """Filtrer les interventions selon les critères."""
    filtered = interventions
    
    # Filtre par statut
    if status_filter != "Tous":
        filtered = [i for i in filtered if i.get('statut') == status_filter]
    
    # Filtre par date (aujourd'hui seulement)
    if today_only:
        today = date.today().isoformat()
        filtered = [i for i in filtered if i.get('date_prevue', '').startswith(today)]
    
    return filtered

def show_intervention_card(intervention: Dict):
    """Afficher une carte d'intervention."""
    # Déterminer la couleur selon le statut
    status_colors = {
        "planifiee": "🟡",
        "en_cours": "🔵", 
        "terminee": "🟢",
        "annulee": "🔴"
    }
    
    status_names = {
        "planifiee": "Planifiée",
        "en_cours": "En cours",
        "terminee": "Terminée", 
        "annulee": "Annulée"
    }
    
    status = intervention.get('statut', 'planifiee')
    status_icon = status_colors.get(status, "⚪")
    status_name = status_names.get(status, status)
    
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
        
        with col1:
            st.markdown(f"**🏥 {intervention.get('patient_id', 'N/A')}**")
            st.markdown(f"🔧 {intervention.get('type_intervention', 'N/A')}")
            if intervention.get('description'):
                st.caption(f"📝 {intervention['description'][:100]}...")
        
        with col2:
            date_str = intervention.get('date_prevue', '')
            if date_str:
                try:
                    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    st.markdown(f"📅 {dt.strftime('%d/%m/%Y')}")
                    st.markdown(f"🕐 {dt.strftime('%H:%M')}")
                except:
                    st.markdown(f"📅 {date_str}")
            
            if intervention.get('duree_estimee'):
                st.markdown(f"⏱️ {intervention['duree_estimee']} min")
        
        with col3:
            st.markdown(f"{status_icon} **{status_name}**")
            if intervention.get('patient_age'):
                st.markdown(f"👤 {intervention['patient_age']} ans")
        
        with col4:
            # Boutons d'action
            if st.button("✏️", key=f"edit_{intervention.get('id')}", help="Modifier"):
                st.session_state.edit_intervention_id = intervention.get('id')
                st.session_state.show_intervention_form = True
                st.rerun()
            
            if st.button("🗑️", key=f"delete_{intervention.get('id')}", help="Supprimer"):
                if st.session_state.get(f"confirm_delete_{intervention.get('id')}"):
                    delete_intervention(intervention.get('id'))
                else:
                    st.session_state[f"confirm_delete_{intervention.get('id')}"] = True
                    st.warning("⚠️ Cliquez à nouveau pour confirmer la suppression")
                    st.rerun()
        
        st.markdown("---")

def delete_intervention(intervention_id: int):
    """Supprimer une intervention."""
    with st.spinner("🗑️ Suppression en cours..."):
        try:
            success = api_client.delete_intervention(intervention_id)
            if success:
                st.success("✅ Intervention supprimée avec succès!")
                # Nettoyer les états de confirmation
                keys_to_remove = [k for k in st.session_state.keys() if k.startswith(f"confirm_delete_{intervention_id}")]
                for key in keys_to_remove:
                    del st.session_state[key]
                st.rerun()
            else:
                st.error("❌ Erreur lors de la suppression")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def show_mock_interventions():
    """Afficher des interventions simulées en cas d'erreur API."""
    st.info("📡 Mode hors ligne - Données simulées")
    
    mock_interventions = [
        {
            "id": 1,
            "patient_id": "PAT-2024-001",
            "type_intervention": "Angioplastie coronaire",
            "date_prevue": "2024-01-15T08:00:00",
            "duree_estimee": 90,
            "patient_age": 65,
            "statut": "planifiee",
            "description": "Angioplastie de l'artère coronaire droite avec pose de stent"
        },
        {
            "id": 2,
            "patient_id": "PAT-2024-002", 
            "type_intervention": "Embolisation utérine",
            "date_prevue": "2024-01-15T10:30:00",
            "duree_estimee": 60,
            "patient_age": 45,
            "statut": "en_cours",
            "description": "Embolisation des artères utérines pour fibromes"
        },
        {
            "id": 3,
            "patient_id": "PAT-2024-003",
            "type_intervention": "Biopsie hépatique",
            "date_prevue": "2024-01-15T14:00:00", 
            "duree_estimee": 30,
            "patient_age": 58,
            "statut": "planifiee",
            "description": "Biopsie percutanée du foie sous guidage échographique"
        }
    ]
    
    for intervention in mock_interventions:
        show_intervention_card(intervention)