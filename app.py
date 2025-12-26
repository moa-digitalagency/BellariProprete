from flask import Flask
from flask_login import LoginManager
from models import db, Admin
from utils import get_settings
from routes import register_routes
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bellari-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.context_processor
def inject_settings():
    return {'settings': get_settings()}

with app.app_context():
    db.create_all()
    
    if not Admin.query.first():
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    
    from models import SiteSettings
    if not SiteSettings.query.first():
        db.session.add(SiteSettings())
        db.session.commit()
    
    from models import Service
    if not Service.query.first():
        from utils import generate_random_image
        services_data = [
            {'title': 'Nettoyage Fin de Chantier', 'description': 'Service spécialisé dans le nettoyage après travaux. Éliminez tous les débris, poussières et résidus de chantier pour une livraison parfaite.', 'icon': 'hard-hat', 'featured': True, 'order': 1},
            {'title': 'Nettoyage d\'Appartements', 'description': 'Entretien professionnel de vos appartements avec produits de qualité. Service complet pour un logement impeccable.', 'icon': 'home', 'featured': True, 'order': 2},
            {'title': 'Nettoyage de Bureau', 'description': 'Maintien d\'un environnement de travail propre et professionnel. Service régulier ou occasionnel pour vos bureaux.', 'icon': 'building-2', 'featured': True, 'order': 3},
            {'title': 'Nettoyage Fin d\'Événement', 'description': 'Nettoyage complet après événements. Remise en état rapide et efficace des lieux après vos festivités.', 'icon': 'sparkles', 'order': 4},
        ]
        for data in services_data:
            image = generate_random_image(filename=f"service_{data['title'].lower().replace(' ', '_')}.jpg")
            service = Service(**data, image=image)
            db.session.add(service)
        db.session.commit()

register_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
