# 🏥 Radiologie Interventionnelle SaaS

Application SaaS pour la gestion des services de radiologie interventionnelle. Ce projet fournit un squelette propre et minimal prêt pour le développement d'un système complet de gestion des interventions, procédures, et feedbacks.

## 🎯 Objectifs

- **Planification** : Gestion des interventions et salles
- **Procédures** : Standardisation des protocoles
- **Feedbacks** : Retours d'expérience et amélioration continue
- **Tableau de bord** : Métriques et suivi des performances

## 🏗️ Architecture

```
radiologie-saas/
├── backend/                 # API FastAPI
│   ├── models/             # Modèles SQLAlchemy
│   ├── schemas/            # Schémas Pydantic
│   ├── routers/            # Routeurs FastAPI
│   └── main.py             # Application principale
├── frontend/               # Interface Streamlit
│   └── app.py              # Application principale
├── database/               # Scripts base de données
│   ├── init_db.py          # Initialisation
│   └── .env.example        # Variables d'environnement
└── requirements.txt        # Dépendances Python
```

## 🛠️ Technologies

- **Backend** : FastAPI, SQLAlchemy, PostgreSQL
- **Frontend** : Streamlit
- **Authentification** : JWT
- **Base de données** : PostgreSQL

## 📋 Prérequis

- Python 3.8+
- PostgreSQL 12+
- pip (gestionnaire de paquets Python)

## 🚀 Installation

### 1. Cloner le repository

```bash
git clone <votre-repository>
cd radiologie-saas
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configuration de la base de données

#### Installer PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS avec Homebrew
brew install postgresql

# Windows : Télécharger depuis https://www.postgresql.org/download/
```

#### Créer la base de données
```bash
sudo -u postgres psql
CREATE DATABASE radiologie_db;
CREATE USER postgres WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE radiologie_db TO postgres;
\q
```

### 4. Configuration des variables d'environnement

```bash
# Copier le fichier d'exemple
cp database/.env.example .env

# Éditer le fichier .env avec vos paramètres
nano .env
```

### 5. Initialiser la base de données

```bash
python database/init_db.py
```

Le script vous demandera si vous souhaitez insérer des données d'exemple (recommandé pour les tests).

## 🎮 Utilisation

### Démarrer le backend (API)

```bash
uvicorn backend.main:app --reload
```

L'API sera accessible à : http://localhost:8000

- Documentation interactive : http://localhost:8000/docs
- Documentation alternative : http://localhost:8000/redoc

### Démarrer le frontend (Interface)

```bash
streamlit run frontend/app.py
```

L'interface sera accessible à : http://localhost:8501

## 👥 Comptes de test

Si vous avez inséré les données d'exemple, vous pouvez utiliser ces comptes :

| Email | Mot de passe | Rôle |
|-------|--------------|------|
| admin@hopital.fr | admin123 | Administrateur |
| martin.dupont@hopital.fr | medecin123 | Médecin |
| sophie.martin@hopital.fr | infirmier123 | Infirmier |
| pierre.durand@hopital.fr | tech123 | Technicien |

## 📚 Structure des données

### Modèles principaux

- **User** : Gestion des utilisateurs et authentification
- **Salle** : Salles d'intervention et équipements
- **Intervention** : Planification des interventions
- **Procedure** : Procédures standardisées
- **CheckList** : Vérifications pré/post intervention
- **Feedback** : Retours d'expérience

### Endpoints API principaux

```
POST /auth/register      # Inscription
POST /auth/login         # Connexion
GET  /auth/me           # Profil utilisateur
GET  /api/interventions # Liste des interventions
GET  /api/salles        # Liste des salles
GET  /api/procedures    # Liste des procédures
GET  /api/checklists    # Liste des checklists
GET  /api/feedbacks     # Liste des feedbacks
```

## 🔧 Développement

### Structure du projet

- `backend/models/` : Modèles de données SQLAlchemy
- `backend/schemas/` : Schémas de validation Pydantic
- `backend/routers/` : Logique des endpoints FastAPI
- `frontend/app.py` : Interface utilisateur Streamlit

### Ajouter de nouvelles fonctionnalités

1. **Nouveau modèle** : Créer dans `backend/models/`
2. **Nouveau schéma** : Créer dans `backend/schemas/`
3. **Nouveaux endpoints** : Ajouter dans `backend/routers/`
4. **Nouvelle interface** : Modifier `frontend/app.py`

### Tests

```bash
# Lancer les tests (à implémenter)
pytest

# Vérifier le code
flake8 backend/ frontend/
```

## 🚨 Sécurité

⚠️ **Important pour la production** :

1. Changer la `SECRET_KEY` dans les variables d'environnement
2. Utiliser des mots de passe forts pour la base de données
3. Configurer HTTPS
4. Implémenter la validation des rôles
5. Ajouter des logs de sécurité
6. Configurer un pare-feu

## 📈 Roadmap

### Phase 1 (MVP) ✅
- [x] Architecture de base
- [x] Authentification JWT
- [x] Modèles de données
- [x] Interface Streamlit basique

### Phase 2 (Développement)
- [ ] CRUD complet pour tous les modèles
- [ ] Gestion des permissions par rôle
- [ ] Notifications en temps réel
- [ ] Export de données

### Phase 3 (Production)
- [ ] Tests automatisés
- [ ] Documentation API complète
- [ ] Monitoring et logs
- [ ] Déploiement Docker

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit les changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créer une Pull Request

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🆘 Support

- **Issues** : Utiliser GitHub Issues pour les bugs et demandes de fonctionnalités
- **Documentation** : Consulter les docstrings dans le code
- **API** : Documentation interactive disponible à `/docs`

## 🔗 Liens utiles

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Note** : Cette application est un MVP (Minimum Viable Product) conçu pour valider l'architecture. Elle ne doit pas être utilisée en production sans les sécurisations et validations appropriées pour un environnement médical.