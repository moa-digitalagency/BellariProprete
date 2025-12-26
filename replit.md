# Bellari Propreté Services - Version 2.0

## Architecture Refactorée

### Structure Modulaire
```
app/
├── __init__.py           # Factory pattern, DB init
├── models/               # Modèles SQLAlchemy
│   ├── admin.py
│   ├── service.py
│   ├── message.py
│   ├── testimonial.py
│   └── settings.py
├── routes/               # Blueprints des routes
│   ├── public.py         # Pages publiques
│   └── admin.py          # Panel admin
├── services/             # Logique métier
│   └── service_manager.py
├── utils/                # Utilitaires
│   ├── helpers.py
│   └── image_generator.py (Génération d'images PIL)
├── security/             # Sécurité
└── templates/            # Templates Jinja2
    ├── public/
    └── admin/
```

### Base de Données PostgreSQL
- **Admin**: Gestion des utilisateurs admin
- **Service**: Services avec SEO, images, vedettes
- **ContactMessage**: Messages de contact
- **Testimonial**: Témoignages clients
- **SiteSettings**: Configuration du site
- **SEOSettings**: SEO par page

## Fonctionnalités Principales

### Site Public
- ✅ Page d'accueil avec services en vedette
- ✅ Page services détaillée avec images aléatoires
- ✅ Page contact fonctionnelle
- ✅ Pages de détails pour chaque service
- ✅ Témoignages clients approuvés
- ✅ Navigation responsive

### Panel Admin Complet
- ✅ Dashboard avec statistiques
- ✅ Gestion des messages (lecture, suppression)
- ✅ Gestion complète des services
  - Ajout/modification/suppression
  - Images générées automatiquement
  - Ordre d'affichage
  - Vedettes (featured)
  - SEO individuel
- ✅ Gestion des témoignages
  - Approbation avant publication
- ✅ Paramètres du site
  - Contact, réseaux sociaux
  - Couleurs personnalisables
- ✅ Gestion SEO
  - Meta descriptions
  - Mots-clés
  - Images meta

### Génération d'Images
- Images aléatoires colorées avec PIL
- Images spécifiques par service (nettoyage de chantier, etc.)
- Génération automatique lors de création de service

## Accès Admin
- **URL**: `/admin/login`
- **Identifiant**: `admin`
- **Mot de passe**: `admin123`

## Mise en avant du Nettoyage de Chantier
- Service en vedette sur page d'accueil
- Ordre prioritaire (ordre = 1)
- Image spécifique générée automatiquement
- Section "Nettoyage de Chantier Professionnel" en héro

## Déploiement
- **Dev**: `python run.py`
- **Production**: `gunicorn wsgi:app`
- **Port**: 5000

## Technologies
- Flask (Backend)
- SQLAlchemy (ORM)
- PostgreSQL (DB)
- Tailwind CSS (Frontend)
- PIL/Pillow (Image generation)
- Flask-Login (Auth)
