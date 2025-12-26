# Bellari Propreté Services

## Overview
Site web professionnel pour Bellari Propreté Services, entreprise de nettoyage spécialisée au Maroc.

## Architecture
- **Backend**: Python Flask
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Base de données**: PostgreSQL

## Structure du projet
```
├── app.py                 # Application Flask principale
├── templates/
│   ├── base.html          # Template de base
│   ├── index.html         # Page d'accueil
│   ├── services.html      # Page services
│   ├── contact.html       # Page contact
│   └── admin/             # Panneau d'administration
│       ├── base.html
│       ├── login.html
│       ├── dashboard.html
│       ├── messages.html
│       ├── services.html
│       ├── testimonials.html
│       └── settings.html
└── static/                # Fichiers statiques
```

## Fonctionnalités
- Site vitrine moderne avec Tailwind CSS
- Formulaire de contact avec stockage en base de données
- Panneau d'administration complet
  - Gestion des messages
  - Gestion des services
  - Gestion des témoignages
  - Paramètres du site

## Accès admin
- URL: /admin/login
- Identifiants par défaut: admin / admin123

## Développement
- Port: 5000
- Commande: `python app.py`
