# Bellari Propreté Services - Version 2.1

## Structure Organisée avec Dossiers

### Arborescence
```
/
├── app.py                   # Application Flask principale
├── run.py                   # Point d'entrée développement
├── wsgi.py                  # Production (gunicorn)
├── models/                  # Modèles SQLAlchemy
│   └── __init__.py
├── routes/                  # Routes et logique des vues
│   └── __init__.py
├── services/                # Logique métier
│   └── __init__.py
├── utils/                   # Utilitaires (génération images, etc)
│   └── __init__.py
├── security/                # Sécurité (authentification)
│   └── __init__.py
├── templates/               # Templates Jinja2
│   ├── public/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── services.html
│   │   ├── service_detail.html
│   │   └── contact.html
│   └── admin/
│       ├── login.html
│       ├── base.html
│       ├── dashboard.html
│       ├── messages.html
│       ├── services.html
│       ├── service_form.html
│       ├── testimonials.html
│       ├── testimonial_form.html
│       ├── settings.html
│       ├── seo.html
│       └── seo_form.html
└── static/
    └── images/              # Images générées automatiquement
```

## Base de Données PostgreSQL
- **Admin**: Authentification utilisateurs
- **Service**: 4 services avec images et SEO
- **ContactMessage**: Messages de contact
- **Testimonial**: Témoignages clients approuvés
- **SiteSettings**: Configuration du site
- **SEOSettings**: Gestion SEO par page

## 4 Services Principaux

### 1. Nettoyage Fin de Chantier ⭐ (VEDETTE - Ordre 1)
- Description: Service spécialisé dans le nettoyage après travaux
- Image: Générée automatiquement
- Featured: OUI

### 2. Nettoyage d'Appartements (VEDETTE - Ordre 2)
- Description: Entretien professionnel avec produits de qualité
- Image: Générée automatiquement
- Featured: OUI

### 3. Nettoyage de Bureau (VEDETTE - Ordre 3)
- Description: Environnement de travail propre et professionnel
- Image: Générée automatiquement
- Featured: OUI

### 4. Nettoyage Fin d'Événement (Ordre 4)
- Description: Remise en état après événements
- Image: Générée automatiquement

## Accès Admin
- **URL**: `/admin/login`
- **Identifiants**: `admin` / `admin123`

### Fonctionnalités Admin
- Dashboard avec statistiques
- Gestion des messages de contact
- Gestion complète des services (CRUD + SEO)
- Gestion des témoignages (approbation)
- Paramètres du site (contact, réseaux sociaux)
- Gestion SEO par page

## Déploiement
- **Dev**: `python run.py`
- **Production**: `gunicorn wsgi:app`
- **Port**: 5000

## Technologies
- Flask
- SQLAlchemy + PostgreSQL
- Pillow (générateur d'images)
- Flask-Login (authentification)
- Tailwind CSS (responsive)
