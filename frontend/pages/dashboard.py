"""
Tableau de bord principal avec métriques et analyses.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from frontend.utils.api_client import api_client

def show_dashboard_page():
    """Afficher le tableau de bord principal."""
    st.header("📊 Tableau de Bord - Radiologie Interventionnelle")
    
    # Récupérer les données
    data = load_dashboard_data()
    
    # Métriques principales
    show_main_metrics(data)
    
    st.markdown("---")
    
    # Graphiques et analyses
    col1, col2 = st.columns(2)
    
    with col1:
        show_interventions_chart(data)
        show_feedback_distribution(data)
    
    with col2:
        show_procedures_usage(data)
        show_satisfaction_trend(data)
    
    st.markdown("---")
    
    # Sections détaillées
    show_detailed_sections(data)

def load_dashboard_data() -> Dict:
    """Charger toutes les données nécessaires pour le dashboard."""
    data = {
        'interventions': [],
        'procedures': [],
        'feedbacks': [],
        'salles': []
    }
    
    try:
        with st.spinner("📊 Chargement des données..."):
            # Charger les données depuis l'API
            data['interventions'] = api_client.get_interventions() or []
            data['procedures'] = api_client.get_procedures() or []
            data['feedbacks'] = api_client.get_feedbacks() or []
            data['salles'] = api_client.get_salles() or []
            
    except Exception as e:
        st.warning(f"⚠️ Erreur de chargement des données: {str(e)}")
        # Utiliser des données simulées en cas d'erreur
        data = get_mock_dashboard_data()
    
    # Si pas de données, utiliser des données simulées
    if not any(data.values()):
        data = get_mock_dashboard_data()
        st.info("📡 Utilisation de données simulées pour la démonstration")
    
    return data

def show_main_metrics(data: Dict):
    """Afficher les métriques principales."""
    st.subheader("📈 Vue d'ensemble")
    
    # Calculer les métriques
    interventions = data['interventions']
    feedbacks = data['feedbacks']
    salles = data['salles']
    
    # Interventions aujourd'hui
    today = date.today().isoformat()
    interventions_today = len([i for i in interventions if i.get('date_prevue', '').startswith(today)])
    
    # Interventions en cours
    interventions_en_cours = len([i for i in interventions if i.get('statut') == 'en_cours'])
    
    # Note moyenne des feedbacks
    notes = [f.get('note_globale', 0) for f in feedbacks if f.get('note_globale')]
    note_moyenne = round(sum(notes) / len(notes), 1) if notes else 0
    
    # Salles actives
    salles_actives = len([s for s in salles if s.get('is_active', True)])
    total_salles = len(salles)
    
    # Affichage des métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "🏥 Interventions aujourd'hui",
            interventions_today,
            delta=f"+{interventions_today - 8}" if interventions_today > 8 else None
        )
    
    with col2:
        st.metric(
            "🔄 En cours",
            interventions_en_cours,
            delta=f"+{interventions_en_cours}" if interventions_en_cours > 0 else None
        )
    
    with col3:
        st.metric(
            "⭐ Satisfaction",
            f"{note_moyenne}/5" if note_moyenne > 0 else "N/A",
            delta=f"+{0.2}" if note_moyenne > 4 else None
        )
    
    with col4:
        st.metric(
            "🏥 Salles actives",
            f"{salles_actives}/{total_salles}",
            delta=None
        )

def show_interventions_chart(data: Dict):
    """Graphique des interventions par statut."""
    st.subheader("📋 Interventions par statut")
    
    interventions = data['interventions']
    
    if not interventions:
        st.info("Aucune donnée d'intervention disponible")
        return
    
    # Compter par statut
    statuts = {}
    for intervention in interventions:
        statut = intervention.get('statut', 'planifiee')
        statuts[statut] = statuts.get(statut, 0) + 1
    
    # Créer le graphique
    if statuts:
        df_statuts = pd.DataFrame(list(statuts.items()), columns=['Statut', 'Nombre'])
        
        # Mapper les statuts pour l'affichage
        status_map = {
            'planifiee': 'Planifiées',
            'en_cours': 'En cours',
            'terminee': 'Terminées',
            'annulee': 'Annulées'
        }
        df_statuts['Statut'] = df_statuts['Statut'].map(status_map)
        
        fig = px.pie(df_statuts, values='Nombre', names='Statut', 
                    color_discrete_map={
                        'Planifiées': '#FFA500',
                        'En cours': '#4169E1', 
                        'Terminées': '#32CD32',
                        'Annulées': '#DC143C'
                    })
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de statut disponible")

def show_procedures_usage(data: Dict):
    """Graphique d'utilisation des procédures."""
    st.subheader("🔧 Procédures les plus utilisées")
    
    interventions = data['interventions']
    
    if not interventions:
        st.info("Aucune donnée d'intervention disponible")
        return
    
    # Compter les types d'interventions
    types = {}
    for intervention in interventions:
        type_intervention = intervention.get('type_intervention', 'Inconnu')
        types[type_intervention] = types.get(type_intervention, 0) + 1
    
    if types:
        # Prendre les 5 plus utilisées
        top_types = sorted(types.items(), key=lambda x: x[1], reverse=True)[:5]
        df_types = pd.DataFrame(top_types, columns=['Procédure', 'Utilisations'])
        
        fig = px.bar(df_types, x='Utilisations', y='Procédure', orientation='h')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de procédure disponible")

def show_feedback_distribution(data: Dict):
    """Distribution des feedbacks par type."""
    st.subheader("💬 Types de feedbacks")
    
    feedbacks = data['feedbacks']
    
    if not feedbacks:
        st.info("Aucun feedback disponible")
        return
    
    # Compter par type
    types_feedback = {}
    for feedback in feedbacks:
        type_fb = feedback.get('type_feedback', 'qualite')
        types_feedback[type_fb] = types_feedback.get(type_fb, 0) + 1
    
    if types_feedback:
        # Mapper les types pour l'affichage
        type_map = {
            'qualite': 'Qualité',
            'securite': 'Sécurité',
            'amelioration': 'Amélioration',
            'incident': 'Incident'
        }
        
        df_feedback = pd.DataFrame(list(types_feedback.items()), columns=['Type', 'Nombre'])
        df_feedback['Type'] = df_feedback['Type'].map(type_map)
        
        fig = px.bar(df_feedback, x='Type', y='Nombre',
                    color='Type',
                    color_discrete_map={
                        'Qualité': '#32CD32',
                        'Amélioration': '#4169E1',
                        'Sécurité': '#FFA500',
                        'Incident': '#DC143C'
                    })
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée de feedback disponible")

def show_satisfaction_trend(data: Dict):
    """Tendance de satisfaction sur le temps."""
    st.subheader("📈 Évolution satisfaction")
    
    # Pour le MVP, on simule une tendance
    dates = pd.date_range(start='2024-01-01', end='2024-01-15', freq='D')
    satisfaction = [4.1, 4.2, 4.0, 4.3, 4.1, 4.4, 4.2, 4.5, 4.3, 4.4, 4.6, 4.5, 4.4, 4.7, 4.6]
    
    df_satisfaction = pd.DataFrame({
        'Date': dates,
        'Satisfaction': satisfaction
    })
    
    fig = px.line(df_satisfaction, x='Date', y='Satisfaction',
                  title='Note moyenne sur 15 jours')
    fig.update_layout(height=300)
    fig.update_yaxis(range=[3.5, 5])
    st.plotly_chart(fig, use_container_width=True)

def show_detailed_sections(data: Dict):
    """Sections détaillées du dashboard."""
    
    # Onglets pour les détails
    tab1, tab2, tab3, tab4 = st.tabs(["🏥 Activité", "⚠️ Alertes", "📊 Performance", "🎯 Objectifs"])
    
    with tab1:
        show_activity_details(data)
    
    with tab2:
        show_alerts_section(data)
    
    with tab3:
        show_performance_metrics(data)
    
    with tab4:
        show_objectives_section(data)

def show_activity_details(data: Dict):
    """Détails de l'activité."""
    st.subheader("🏥 Détails de l'activité")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**📅 Interventions de la semaine**")
        
        # Simuler les données de la semaine
        jours = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
        interventions_semaine = [12, 15, 18, 14, 16, 8, 5]
        
        df_semaine = pd.DataFrame({
            'Jour': jours,
            'Interventions': interventions_semaine
        })
        
        fig = px.bar(df_semaine, x='Jour', y='Interventions')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**⏱️ Durées moyennes par type**")
        
        # Calculer les durées moyennes réelles ou simulées
        durees_types = {
            'Angioplastie': 95,
            'Embolisation': 65,
            'Biopsie': 35,
            'Stent': 45
        }
        
        df_durees = pd.DataFrame(list(durees_types.items()), columns=['Type', 'Durée (min)'])
        
        fig = px.bar(df_durees, x='Type', y='Durée (min)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

def show_alerts_section(data: Dict):
    """Section des alertes et notifications."""
    st.subheader("⚠️ Alertes et notifications")
    
    # Alertes simulées
    alertes = [
        {"type": "warning", "message": "Salle 2: Maintenance programmée demain", "priority": "Moyenne"},
        {"type": "info", "message": "3 nouveaux feedbacks à traiter", "priority": "Faible"},
        {"type": "error", "message": "Incident signalé en salle 1", "priority": "Haute"},
        {"type": "success", "message": "Objectif satisfaction atteint ce mois", "priority": "Info"}
    ]
    
    for alerte in alertes:
        if alerte["type"] == "error":
            st.error(f"🚨 **{alerte['priority']}**: {alerte['message']}")
        elif alerte["type"] == "warning":
            st.warning(f"⚠️ **{alerte['priority']}**: {alerte['message']}")
        elif alerte["type"] == "info":
            st.info(f"ℹ️ **{alerte['priority']}**: {alerte['message']}")
        elif alerte["type"] == "success":
            st.success(f"✅ **{alerte['priority']}**: {alerte['message']}")

def show_performance_metrics(data: Dict):
    """Métriques de performance détaillées."""
    st.subheader("📊 Indicateurs de performance")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**⏱️ Temps d'intervention**")
        st.metric("Temps moyen", "75 min", "-5 min")
        st.metric("Respect planning", "92%", "+3%")
        st.metric("Retards > 30min", "8%", "-2%")
    
    with col2:
        st.markdown("**👥 Équipe**")
        st.metric("Taux présence", "96%", "+1%")
        st.metric("Formations validées", "85%", "+5%")
        st.metric("Rotations équipes", "12", "0")
    
    with col3:
        st.markdown("**🏥 Matériel**")
        st.metric("Disponibilité", "98%", "0%")
        st.metric("Pannes signalées", "2", "-1")
        st.metric("Maintenance préventive", "100%", "0%")

def show_objectives_section(data: Dict):
    """Section des objectifs et KPI."""
    st.subheader("🎯 Objectifs et indicateurs clés")
    
    # Objectifs avec barres de progression
    objectifs = [
        {"nom": "Satisfaction patient", "actuel": 4.6, "cible": 4.5, "unite": "/5"},
        {"nom": "Temps intervention", "actuel": 75, "cible": 80, "unite": "min"},
        {"nom": "Taux d'incidents", "actuel": 2, "cible": 5, "unite": "%"},
        {"nom": "Formation équipe", "actuel": 85, "cible": 90, "unite": "%"}
    ]
    
    for obj in objectifs:
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.markdown(f"**{obj['nom']}**")
        
        with col2:
            # Calculer le pourcentage d'atteinte
            if obj['nom'] == "Temps intervention" or obj['nom'] == "Taux d'incidents":
                # Pour ces métriques, plus c'est bas, mieux c'est
                progress = min(100, (obj['cible'] / obj['actuel']) * 100) if obj['actuel'] > 0 else 0
            else:
                # Pour ces métriques, plus c'est haut, mieux c'est
                progress = min(100, (obj['actuel'] / obj['cible']) * 100) if obj['cible'] > 0 else 0
            
            st.progress(progress / 100)
        
        with col3:
            couleur = "🟢" if progress >= 90 else "🟡" if progress >= 70 else "🔴"
            st.markdown(f"{couleur} {obj['actuel']}{obj['unite']}")

def get_mock_dashboard_data() -> Dict:
    """Données simulées pour le dashboard."""
    return {
        'interventions': [
            {
                "id": 1,
                "patient_id": "PAT-2024-001",
                "type_intervention": "Angioplastie coronaire",
                "date_prevue": f"{date.today().isoformat()}T08:00:00",
                "duree_estimee": 90,
                "statut": "planifiee"
            },
            {
                "id": 2,
                "patient_id": "PAT-2024-002",
                "type_intervention": "Embolisation utérine",
                "date_prevue": f"{date.today().isoformat()}T10:30:00",
                "duree_estimee": 60,
                "statut": "en_cours"
            },
            {
                "id": 3,
                "patient_id": "PAT-2024-003",
                "type_intervention": "Biopsie hépatique",
                "date_prevue": f"{(date.today() - timedelta(days=1)).isoformat()}T14:00:00",
                "duree_estimee": 30,
                "statut": "terminee"
            }
        ],
        'feedbacks': [
            {
                "id": 1,
                "type_feedback": "qualite",
                "titre": "Excellente coordination",
                "note_globale": 5
            },
            {
                "id": 2,
                "type_feedback": "amelioration",
                "titre": "Optimiser préparation",
                "note_globale": 4
            },
            {
                "id": 3,
                "type_feedback": "incident",
                "titre": "Problème technique mineur",
                "note_globale": 3
            }
        ],
        'salles': [
            {"id": 1, "nom": "Salle 1", "is_active": True},
            {"id": 2, "nom": "Salle 2", "is_active": True},
            {"id": 3, "nom": "Salle 3", "is_active": False}
        ],
        'procedures': [
            {"id": 1, "nom": "Angioplastie coronaire"},
            {"id": 2, "nom": "Embolisation utérine"},
            {"id": 3, "nom": "Biopsie hépatique"}
        ]
    }