from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def init_login_manager(app):
    from app.models import Admin
    
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bellari-secret-key-2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    init_login_manager(app)
    
    with app.app_context():
        from app.models import Admin, Service, ContactMessage, Testimonial, SiteSettings, SEOSettings
        
        db.create_all()
        
        from app.routes.admin import admin_bp
        from app.routes.public import public_bp
        
        app.register_blueprint(admin_bp)
        app.register_blueprint(public_bp)
        
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        if not SiteSettings.query.first():
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        
        if not Service.query.first():
            services_data = [
                {'title': 'Nettoyage de Chantier', 'description': 'Pour la qualité et la sécurité de vos chantiers, nous proposons un service de nettoyage professionnel tout au long de la durée du projet.', 'icon': 'hard-hat', 'image': 'chantier.jpg', 'featured': True, 'order': 1},
                {'title': 'Nettoyage Fin de Chantier', 'description': 'Avant la livraison de vos projets, un nettoyage avec finition impeccable est indispensable pour garantir une présentation parfaite.', 'icon': 'sparkles', 'image': 'fin_chantier.jpg', 'featured': True, 'order': 2},
                {'title': 'Entretien Post-Livraison', 'description': 'Après la livraison, un entretien régulier est indispensable. Nous vous accompagnons pour une sérénité au quotidien.', 'icon': 'home', 'image': 'entretien.jpg', 'order': 3},
                {'title': 'Nettoyage de Villas', 'description': 'Services complets de nettoyage pour villas incluant sols, murs, vitres et espaces extérieurs.', 'icon': 'home', 'image': 'villa.jpg', 'order': 4},
                {'title': 'Nettoyage d\'Appartements', 'description': 'Entretien professionnel de vos appartements avec des produits de qualité et des techniques adaptées.', 'icon': 'building', 'image': 'appartement.jpg', 'order': 5},
                {'title': 'Nettoyage de Vitres', 'description': 'Nettoyage professionnel de toutes vos surfaces vitrées pour une transparence parfaite.', 'icon': 'sparkles', 'image': 'vitres.jpg', 'order': 6}
            ]
            for data in services_data:
                service = Service(**data)
                db.session.add(service)
            db.session.commit()
        
        if not Testimonial.query.first():
            testimonial = Testimonial(
                name='Mohcine Tazi',
                content='Bellari a transformé notre chantier en un espace propre et accueillant. Service exceptionnel et rapide !',
                rating=5
            )
            db.session.add(testimonial)
            db.session.commit()
    
    @app.context_processor
    def inject_settings():
        try:
            from app.models import SiteSettings
            return {'settings': SiteSettings.query.first()}
        except:
            return {'settings': None}
    
    return app
