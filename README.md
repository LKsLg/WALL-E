Une simulation d'équipe de robots autonomes nettoyant une zone contenant des déchets, inspirée du projet technique WALL-E.

#Description

Cette application simule une équipe de robots collaborant pour nettoyer efficacement une grille 32x32 contenant des déchets. Les robots utilisent des stratégies intelligentes d'exploration et de communication pour optimiser leur travail.

### Fonctionnalités

- Grille 32x32 avec robots, déchets et base
- Robots autonomes avec vision, transport et communication
- Stratégies intelligentes d'exploration et collaboration
- Interface temps réel avec statistiques
- API RESTful complète avec WebSockets
- Configuration flexible du nombre de robots et déchets

# Architecture

## Backend (Django)
- API RESTful avec Django REST Framework
- WebSockets pour les mises à jour temps réel
- Moteur de simulation avec IA des robots
- Système de mémoire et communication inter-robots

## Frontend (React + TypeScript)
- Interface moderne avec Tailwind CSS
- Visualisation temps réel de la grille
- Contrôles de simulation (start/pause/reset)
- Statistiques détaillées

# Installation et Démarrage

## Backend Django

```bash
# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Migrations
python manage.py makemigrations simulation
python manage.py migrate

# Démarrer le serveur
python manage.py runserver
```

## Frontend React

```bash
# Installer les dépendances
npm install

# Démarrer le serveur de développement
npm start
```

L'application sera accessible sur http://localhost:3000

# Utilisation

1. Configuration : Définissez le nombre de robots, déchets et position de la base
2. Création : Créez une nouvelle simulation
3. Contrôle : Utilisez les boutons pour démarrer, mettre en pause ou réinitialiser
4. Observation : Suivez les statistiques et la progression en temps réel

# API Endpoints

- `GET /api/simulations/` - Liste des simulations
- `POST /api/simulations/` - Créer une simulation
- `POST /api/simulations/{id}/start/` - Démarrer
- `POST /api/simulations/{id}/pause/` - Mettre en pause
- `POST /api/simulations/{id}/reset/` - Réinitialiser
- `POST /api/simulations/{id}/step/` - Exécuter une étape
- `GET /api/simulations/{id}/grid_state/` - État de la grille
- `GET /api/simulations/{id}/statistics/` - Statistiques

# Stratégies des Robots

## Exploration Intelligente
- Vision : Rayon de 5 cellules
- Mémoire : Zones explorées et déchets connus
- Priorités : Déchets proches > Exploration > Retour base

## Communication
- Partage d'informations sur les déchets découverts
- Coordination pour éviter les collisions
- Optimisation des trajectoires

