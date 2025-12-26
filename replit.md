# Bellari Propreté Services - Version 2.1

## Architecture Simplifiée - Fichiers à la Racine

### Structure
```
/
├── app.py                   # Application Flask principale
├── models.py                # Modèles SQLAlchemy
├── services.py              # Logique métier
├── utils.py                 # Utilitaires (images)
├── run.py                   # Point d'entrée
├── wsgi.py                  # Production
├── templates/
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
└── static/images/           # Images générées
```

## Base de Données PostgreSQL
- **Admin**: Authentification
- **Service**: 4 services (avec images générées)
- **ContactMessage**: Messages de contact
- **Testimonial**: Témoignages approuvés
- **SiteSettings**: Configuration globale
- **SEOSettings**: Gestion SEO par page

## 4 Services Principaux

### 1. Nettoyage Fin de Chantier (EN VEDETTE - ordre 1)
Description: Service spécialisé dans le nettoyage après travaux. Éliminez tous les débris, poussières et résidus de chantier pour une livraison parfaite.
- Image : Générée automatiquement
- SEO personnalisable
- Featured : OUI

### 2. Nettoyage d'Appartements (EN VEDETTE - ordre 2)
Description: Entretien professionnel de vos appartements avec produits de qualité. Service complet pour un logement impeccable.
- Image : Générée automatiquement
- Featured : OUI

### 3. Nettoyage de Bureau (EN VEDETTE - ordre 3)
Description: Maintien d'un environnement de travail propre et professionnel. Service régulier ou occasionnel pour vos bureaux.
- Image : Générée automatiquement
- Featured : OUI

### 4. Nettoyage Fin d'Événement (ordre 4)
Description: Nettoyage complet après événements. Remise en état rapide et efficace des lieux après vos festivités.
- Image : Générée automatiquement

## Accès Admin
- **URL**: `/admin/login`
- **Identifiants**: `admin` / `admin123`

### Fonctionnalités Admin Complètes
- Dashboard avec statistiques
- Gestion des messages de contact
- Gestion complète des 4 services (CRUD)
- Gestion des témoignages (approbation)
- Paramètres du site (contact, réseaux sociaux, infos)
- Gestion SEO par page

## Page d'Accueil
- Section héro : "Nettoyage Fin de Chantier" (mise en avant)
- 3 services vedette affichés
- Témoignages clients approuvés
- CTA "Demander un devis" / "Tous nos services"
- Bouton WhatsApp flottant

## Génération d'Images
- PIL/Pillow pour images aléatoires colorées
- Générations automatiques lors de création
- Spécifique à chaque service

## Déploiement
- **Dev**: `python run.py`
- **Production**: `gunicorn wsgi:app`
- **Port**: 5000

## Technologies
- Flask 2.x
- SQLAlchemy + PostgreSQL
- Pillow (images)
- Flask-Login (authentification)
- Tailwind CSS (responsive)
