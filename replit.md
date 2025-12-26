# Bellari Propreté Services - Version 2.2

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
│   │   ├── contact.html
│   │   └── devis.html       # Formulaire devis WhatsApp
│   └── admin/
│       ├── login.html
│       ├── base.html
│       ├── dashboard.html
│       ├── messages.html
│       ├── services.html
│       ├── service_form.html
│       ├── testimonials.html
│       ├── testimonial_form.html
│       ├── settings.html    # Paramètres avancés
│       ├── seo.html
│       ├── seo_form.html    # SEO avancé
│       └── images.html      # Gestion des images
└── static/
    └── images/              # Images uploadées et générées
```

## Base de Données PostgreSQL
- **Admin**: Authentification utilisateurs
- **Service**: 4 services avec images et SEO
- **ContactMessage**: Messages de contact
- **Testimonial**: Témoignages clients approuvés
- **SiteSettings**: Configuration avancée du site
- **SEOSettings**: Gestion SEO avancée par page
- **SiteImage**: Images uploadées

## Design
- **Couleur Principale**: Vert foncé #1B4D3D
- **Couleur Secondaire**: Vert clair #7CB342
- **Style**: Moderne, professionnel, responsive

## Fonctionnalités Principales

### Page Devis (/devis)
- Formulaire complet: nom, téléphone, service, adresse, surface, date
- Envoi automatique via WhatsApp au numéro configuré
- Message formaté avec tous les détails

### SiteSettings Avancés
- Informations entreprise (nom, adresse, horaires)
- Contact (téléphone, email, WhatsApp)
- Réseaux sociaux (Facebook, Instagram)
- Couleurs personnalisables
- Images (logo, héro, favicon)
- Analytics (Google Analytics, GTM, Facebook Pixel)
- Code personnalisé (header, footer, Google Maps embed)
- Message WhatsApp par défaut

### SEO Avancé par Page
- Titre et description méta
- Mots-clés
- URL canonique
- Directive robots (index/noindex)
- Open Graph (type, image)
- Twitter Card
- Données structurées JSON-LD
- Code head personnalisé par page

### Gestion des Images
- Upload d'images depuis l'admin
- Catégorisation (héro, services, galerie, équipe)
- Texte alternatif pour SEO
- Suppression avec nettoyage fichier

## Accès Admin
- **URL**: `/admin/login`
- **Identifiants**: `admin` / `admin123`

### Sections Admin
- Dashboard avec statistiques
- Messages de contact
- Services (CRUD + upload image + SEO)
- Témoignages (approbation)
- Images (upload/gestion)
- SEO par page
- Paramètres avancés

## Déploiement
- **Dev**: `python run.py`
- **Production**: `gunicorn wsgi:app`
- **Port**: 5000

## Technologies
- Flask + SQLAlchemy
- PostgreSQL
- Pillow (images)
- Flask-Login (authentification)
- Tailwind CSS (responsive)
