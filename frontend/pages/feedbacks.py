"""
Page de gestion des feedbacks et retours d'expérience.
"""

import streamlit as st
from datetime import datetime, date
from typing import List, Dict, Optional
from frontend.utils.api_client import api_client

def show_feedbacks_page():
    """Afficher la page de gestion des feedbacks."""
    st.header("💬 Feedbacks et Retours d'Expérience")
    
    # Onglets pour organiser les fonctionnalités
    tab1, tab2, tab3 = st.tabs(["📝 Nouveau Feedback", "📋 Consulter", "📊 Analyses"])
    
    with tab1:
        show_feedback_form()
    
    with tab2:
        show_feedbacks_list()
    
    with tab3:
        show_feedback_analytics()

def show_feedback_form():
    """Afficher le formulaire de création de feedback."""
    st.subheader("📝 Créer un nouveau feedback")
    
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Sélection de l'intervention
            intervention_options = get_intervention_options()
            intervention_id = st.selectbox(
                "🏥 Intervention concernée",
                options=list(intervention_options.keys()),
                format_func=lambda x: intervention_options.get(x, "Intervention inconnue"),
                help="Sélectionnez l'intervention pour laquelle vous souhaitez donner un feedback"
            )
            
            type_feedback = st.selectbox(
                "📋 Type de feedback",
                options=["qualite", "securite", "amelioration", "incident"],
                format_func=lambda x: {
                    "qualite": "⭐ Qualité",
                    "securite": "🛡️ Sécurité",
                    "amelioration": "🔧 Amélioration",
                    "incident": "⚠️ Incident"
                }.get(x, x),
                help="Choisissez le type de feedback le plus approprié"
            )
            
            note_globale = st.slider(
                "⭐ Note globale",
                min_value=1,
                max_value=5,
                value=4,
                help="Note de 1 (très insatisfait) à 5 (très satisfait)"
            )
        
        with col2:
            titre = st.text_input(
                "📌 Titre du feedback",
                placeholder="Ex: Excellente coordination équipe",
                help="Titre court et descriptif"
            )
            
            # Niveau de gravité (seulement pour les incidents)
            gravite = None
            if type_feedback == "incident":
                gravite = st.selectbox(
                    "🚨 Niveau de gravité",
                    options=["faible", "moyen", "eleve", "critique"],
                    format_func=lambda x: {
                        "faible": "🟢 Faible",
                        "moyen": "🟡 Moyen",
                        "eleve": "🟠 Élevé",
                        "critique": "🔴 Critique"
                    }.get(x, x)
                )
            
            urgence = st.checkbox("🚨 Feedback urgent", help="Cochez si ce feedback nécessite une attention immédiate")
        
        description = st.text_area(
            "📝 Description détaillée",
            placeholder="Décrivez votre retour d'expérience en détail...",
            height=150,
            help="Soyez aussi précis que possible pour aider à l'amélioration continue"
        )
        
        actions_suggerees = st.text_area(
            "💡 Actions suggérées (optionnel)",
            placeholder="Quelles améliorations proposez-vous ?",
            height=100,
            help="Vos suggestions d'amélioration sont précieuses"
        )
        
        # Ajout de tags
        st.markdown("🏷️ **Tags** (optionnel)")
        col1, col2 = st.columns(2)
        with col1:
            tag_equipe = st.checkbox("👥 Équipe")
            tag_materiel = st.checkbox("🧰 Matériel")
            tag_procedure = st.checkbox("📋 Procédure")
        with col2:
            tag_communication = st.checkbox("💬 Communication")
            tag_formation = st.checkbox("🎓 Formation")
            tag_organisation = st.checkbox("📊 Organisation")
        
        # Boutons d'action
        col1, col2, col3 = st.columns(3)
        with col1:
            submit_btn = st.form_submit_button("💾 Envoyer Feedback", use_container_width=True)
        with col2:
            draft_btn = st.form_submit_button("📄 Sauver Brouillon", use_container_width=True)
        with col3:
            if st.form_submit_button("❌ Annuler", use_container_width=True):
                st.rerun()
        
        if submit_btn and titre and description:
            # Construire les tags
            tags = []
            if tag_equipe: tags.append("équipe")
            if tag_materiel: tags.append("matériel")
            if tag_procedure: tags.append("procédure")
            if tag_communication: tags.append("communication")
            if tag_formation: tags.append("formation")
            if tag_organisation: tags.append("organisation")
            
            feedback_data = {
                "intervention_id": int(intervention_id) if intervention_id != "none" else None,
                "type_feedback": type_feedback,
                "titre": titre,
                "description": description,
                "note_globale": note_globale,
                "gravite": gravite,
                "actions_suggerees": actions_suggerees,
                "tags": tags,
                "urgent": urgence
            }
            
            create_feedback(feedback_data)
        elif submit_btn:
            st.error("⚠️ Le titre et la description sont obligatoires")
        
        if draft_btn:
            st.info("📄 Fonctionnalité 'Brouillon' à implémenter")

def get_intervention_options() -> Dict[str, str]:
    """Récupérer les options d'interventions disponibles."""
    try:
        interventions = api_client.get_interventions()
        if interventions:
            options = {}
            for intervention in interventions[-10:]:  # 10 dernières interventions
                date_str = ""
                if intervention.get('date_prevue'):
                    try:
                        dt = datetime.fromisoformat(intervention['date_prevue'].replace('Z', '+00:00'))
                        date_str = dt.strftime('%d/%m/%Y')
                    except:
                        date_str = intervention['date_prevue'][:10]
                
                label = f"{intervention.get('patient_id', 'N/A')} - {intervention.get('type_intervention', 'N/A')} ({date_str})"
                options[str(intervention['id'])] = label
            
            options["none"] = "❓ Feedback général (non lié à une intervention)"
            return options
        else:
            return {"none": "❓ Aucune intervention disponible"}
    except:
        return {"none": "❌ Erreur chargement interventions"}

def create_feedback(feedback_data: Dict):
    """Créer un nouveau feedback."""
    with st.spinner("💾 Envoi du feedback..."):
        try:
            result = api_client.create_feedback(feedback_data)
            if result:
                st.success("✅ Feedback envoyé avec succès!")
                st.balloons()
                
                # Afficher un message personnalisé selon le type
                if feedback_data['type_feedback'] == 'incident':
                    st.warning("⚠️ Votre signalement d'incident a été transmis à l'équipe de sécurité.")
                elif feedback_data['urgent']:
                    st.info("🚨 Votre feedback urgent sera traité en priorité.")
                
                st.rerun()
            else:
                st.error("❌ Erreur lors de l'envoi du feedback")
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")

def show_feedbacks_list():
    """Afficher la liste des feedbacks."""
    st.subheader("📋 Consulter les feedbacks")
    
    # Filtres
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        filter_type = st.selectbox(
            "Type",
            ["Tous", "qualite", "securite", "amelioration", "incident"],
            format_func=lambda x: {
                "Tous": "📋 Tous",
                "qualite": "⭐ Qualité",
                "securite": "🛡️ Sécurité", 
                "amelioration": "🔧 Amélioration",
                "incident": "⚠️ Incident"
            }.get(x, x)
        )
    
    with col2:
        filter_note = st.selectbox(
            "Note minimum",
            [1, 2, 3, 4, 5],
            index=0,
            format_func=lambda x: f"⭐ {x}+"
        )
    
    with col3:
        filter_date = st.date_input(
            "Depuis le",
            value=date.today().replace(day=1)  # Premier jour du mois
        )
    
    with col4:
        if st.button("🔄 Actualiser", use_container_width=True):
            st.rerun()
    
    # Liste des feedbacks
    with st.spinner("🔄 Chargement des feedbacks..."):
        try:
            feedbacks = api_client.get_feedbacks()
            
            if not feedbacks:
                st.info("📝 Aucun feedback trouvé.")
                show_mock_feedbacks()
                return
            
            # Filtrer les feedbacks
            filtered_feedbacks = filter_feedbacks(feedbacks, filter_type, filter_note, filter_date)
            
            if not filtered_feedbacks:
                st.info("🔍 Aucun feedback ne correspond aux filtres sélectionnés.")
                return
            
            # Afficher les feedbacks
            for feedback in filtered_feedbacks:
                show_feedback_card(feedback)
                
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement: {str(e)}")
            show_mock_feedbacks()

def filter_feedbacks(feedbacks: List[Dict], type_filter: str, min_note: int, since_date: date) -> List[Dict]:
    """Filtrer les feedbacks selon les critères."""
    filtered = feedbacks
    
    # Filtre par type
    if type_filter != "Tous":
        filtered = [f for f in filtered if f.get('type_feedback') == type_filter]
    
    # Filtre par note
    filtered = [f for f in filtered if f.get('note_globale', 0) >= min_note]
    
    # Filtre par date (simplifié pour le MVP)
    # Dans une vraie application, on comparerait avec la date de création
    
    return filtered

def show_feedback_card(feedback: Dict):
    """Afficher une carte de feedback."""
    # Icônes selon le type
    type_icons = {
        "qualite": "⭐",
        "securite": "🛡️",
        "amelioration": "🔧",
        "incident": "⚠️"
    }
    
    type_names = {
        "qualite": "Qualité",
        "securite": "Sécurité",
        "amelioration": "Amélioration", 
        "incident": "Incident"
    }
    
    feedback_type = feedback.get('type_feedback', 'qualite')
    type_icon = type_icons.get(feedback_type, "💬")
    type_name = type_names.get(feedback_type, feedback_type)
    
    with st.container():
        # En-tête
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.markdown(f"**{type_icon} {feedback.get('titre', 'Feedback sans titre')}**")
        with col2:
            note = feedback.get('note_globale', 0)
            stars = "⭐" * note if note > 0 else "❓"
            st.markdown(f"**{stars}**")
        with col3:
            # Date (simulée)
            st.caption("📅 15/01/2024")
        
        # Contenu
        st.markdown(f"**Type:** {type_name}")
        
        if feedback.get('description'):
            st.markdown(f"**Description:** {feedback['description']}")
        
        if feedback.get('actions_suggerees'):
            st.markdown(f"**💡 Actions suggérées:** {feedback['actions_suggerees']}")
        
        # Gravité pour les incidents
        if feedback_type == "incident" and feedback.get('gravite'):
            gravite_icons = {
                "faible": "🟢 Faible",
                "moyen": "🟡 Moyen", 
                "eleve": "🟠 Élevé",
                "critique": "🔴 Critique"
            }
            gravite_text = gravite_icons.get(feedback['gravite'], feedback['gravite'])
            st.markdown(f"**🚨 Gravité:** {gravite_text}")
        
        # Auteur (simulé)
        st.caption(f"👤 Par: {feedback.get('auteur', 'Dr. Martin Dupont')}")
        
        st.markdown("---")

def show_feedback_analytics():
    """Afficher les analyses de feedbacks."""
    st.subheader("📊 Analyses et Statistiques")
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Feedbacks", "47", "8")
    with col2:
        st.metric("Note moyenne", "4.2/5", "0.3")
    with col3:
        st.metric("Incidents signalés", "3", "1")
    with col4:
        st.metric("Actions en cours", "12", "-2")
    
    st.markdown("---")
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Évolution des feedbacks")
        # Données simulées
        import pandas as pd
        chart_data = pd.DataFrame({
            'Date': ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
            'Feedbacks': [8, 12, 15, 12]
        })
        st.bar_chart(chart_data.set_index('Date'))
    
    with col2:
        st.subheader("🎯 Répartition par type")
        type_data = pd.DataFrame({
            'Type': ['Qualité', 'Amélioration', 'Sécurité', 'Incident'],
            'Nombre': [20, 15, 9, 3]
        })
        st.bar_chart(type_data.set_index('Type'))
    
    # Top des améliorations suggérées
    st.subheader("💡 Top des améliorations suggérées")
    ameliorations = [
        "Optimiser le temps de préparation des salles",
        "Améliorer la communication inter-équipes",
        "Standardiser les protocoles de nettoyage",
        "Former sur les nouveaux équipements",
        "Réduire les temps d'attente patients"
    ]
    
    for i, amelioration in enumerate(ameliorations, 1):
        st.markdown(f"{i}. {amelioration}")
    
    # Actions prioritaires
    st.subheader("🎯 Actions prioritaires")
    with st.expander("📋 Actions en cours de traitement"):
        actions = [
            {"titre": "Formation équipe salle 2", "statut": "En cours", "priorite": "Haute"},
            {"titre": "Révision protocole nettoyage", "statut": "Planifié", "priorite": "Moyenne"},
            {"titre": "Achat nouveau matériel", "statut": "Validé", "priorite": "Faible"}
        ]
        
        for action in actions:
            priority_color = {"Haute": "🔴", "Moyenne": "🟡", "Faible": "🟢"}
            st.markdown(f"• **{action['titre']}** - {action['statut']} {priority_color.get(action['priorite'], '')}")

def show_mock_feedbacks():
    """Afficher des feedbacks simulés."""
    st.info("📡 Mode hors ligne - Données simulées")
    
    mock_feedbacks = [
        {
            "id": 1,
            "titre": "Excellente coordination équipe",
            "type_feedback": "qualite",
            "description": "L'équipe a fait preuve d'une coordination exceptionnelle durant l'intervention complexe.",
            "note_globale": 5,
            "actions_suggerees": "Continuer sur cette lancée et partager les bonnes pratiques",
            "auteur": "Dr. Martin Dupont"
        },
        {
            "id": 2,
            "titre": "Problème technique mineur",
            "type_feedback": "incident",
            "description": "Dysfonctionnement temporaire de l'écran de monitoring, résolu rapidement.",
            "note_globale": 3,
            "gravite": "faible",
            "actions_suggerees": "Vérification préventive hebdomadaire du matériel",
            "auteur": "Inf. Sophie Martin"
        },
        {
            "id": 3,
            "titre": "Optimiser temps préparation",
            "type_feedback": "amelioration",
            "description": "Le temps de préparation de la salle pourrait être réduit avec une meilleure organisation.",
            "note_globale": 4,
            "actions_suggerees": "Créer une checklist de préparation standardisée",
            "auteur": "Tech. Pierre Durand"
        }
    ]
    
    for feedback in mock_feedbacks:
        show_feedback_card(feedback)