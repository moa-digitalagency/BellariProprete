import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'bellari-secret-key-2025')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'admin_login'

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='sparkles')
    order = db.Column(db.Integer, default=0)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='Bellari Propreté Services')
    phone = db.Column(db.String(30), default='+212 6 80 76 03 52')
    email = db.Column(db.String(120), default='bellari.groupe@gmail.com')
    whatsapp = db.Column(db.String(30), default='+33774496440')
    facebook = db.Column(db.String(200), default='https://www.facebook.com/profile.php?id=61579236225216')
    instagram = db.Column(db.String(200), default='https://www.instagram.com/shabakainvest/')
    address = db.Column(db.Text, default='Maroc')

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

def get_settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
        db.session.commit()
    return settings

@app.context_processor
def inject_settings():
    try:
        return {'settings': get_settings()}
    except:
        return {'settings': None}

@app.route('/')
def index():
    services = Service.query.order_by(Service.order).all()
    testimonials = Testimonial.query.all()
    settings = get_settings()
    return render_template('index.html', services=services, testimonials=testimonials, settings=settings)

@app.route('/services')
def services():
    services = Service.query.order_by(Service.order).all()
    settings = get_settings()
    return render_template('services.html', services=services, settings=settings)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = get_settings()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        
        new_message = ContactMessage(name=name, email=email, phone=phone, message=message)
        db.session.add(new_message)
        db.session.commit()
        flash('Votre message a été envoyé avec succès!', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html', settings=settings)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Admin.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('Identifiants incorrects', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    messages_count = ContactMessage.query.filter_by(is_read=False).count()
    services_count = Service.query.count()
    testimonials_count = Testimonial.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    return render_template('admin/dashboard.html', 
                         messages_count=messages_count,
                         services_count=services_count,
                         testimonials_count=testimonials_count,
                         recent_messages=recent_messages)

@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/<int:id>/read', methods=['POST'])
@login_required
def mark_message_read(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    return redirect(url_for('admin_messages'))

@app.route('/admin/messages/<int:id>/delete', methods=['POST'])
@login_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message supprimé', 'success')
    return redirect(url_for('admin_messages'))

@app.route('/admin/services')
@login_required
def admin_services():
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services.html', services=services)

@app.route('/admin/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        icon = request.form.get('icon', 'sparkles')
        order = request.form.get('order', 0)
        
        service = Service(title=title, description=description, icon=icon, order=int(order))
        db.session.add(service)
        db.session.commit()
        flash('Service ajouté avec succès', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_form.html', service=None)

@app.route('/admin/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.title = request.form.get('title')
        service.description = request.form.get('description')
        service.icon = request.form.get('icon', 'sparkles')
        service.order = int(request.form.get('order', 0))
        db.session.commit()
        flash('Service modifié avec succès', 'success')
        return redirect(url_for('admin_services'))
    
    return render_template('admin/service_form.html', service=service)

@app.route('/admin/services/<int:id>/delete', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé', 'success')
    return redirect(url_for('admin_services'))

@app.route('/admin/testimonials')
@login_required
def admin_testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@app.route('/admin/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')
        rating = int(request.form.get('rating', 5))
        
        testimonial = Testimonial(name=name, content=content, rating=rating)
        db.session.add(testimonial)
        db.session.commit()
        flash('Témoignage ajouté avec succès', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=None)

@app.route('/admin/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'POST':
        testimonial.name = request.form.get('name')
        testimonial.content = request.form.get('content')
        testimonial.rating = int(request.form.get('rating', 5))
        db.session.commit()
        flash('Témoignage modifié avec succès', 'success')
        return redirect(url_for('admin_testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

@app.route('/admin/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Témoignage supprimé', 'success')
    return redirect(url_for('admin_testimonials'))

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = get_settings()
    
    if request.method == 'POST':
        settings.company_name = request.form.get('company_name')
        settings.phone = request.form.get('phone')
        settings.email = request.form.get('email')
        settings.whatsapp = request.form.get('whatsapp')
        settings.facebook = request.form.get('facebook')
        settings.instagram = request.form.get('instagram')
        settings.address = request.form.get('address')
        db.session.commit()
        flash('Paramètres mis à jour avec succès', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', settings=settings)

def init_db():
    with app.app_context():
        db.create_all()
        
        if not Admin.query.first():
            admin = Admin(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
        
        if not Service.query.first():
            services_data = [
                {'title': 'Nettoyage de Chantier', 'description': 'Pour la qualité et la sécurité de vos chantiers, nous proposons un service de nettoyage professionnel tout au long de la durée du projet.', 'icon': 'building', 'order': 1},
                {'title': 'Nettoyage Fin de Chantier', 'description': 'Avant la livraison de vos projets, un nettoyage avec finition impeccable est indispensable pour garantir une présentation parfaite.', 'icon': 'sparkles', 'order': 2},
                {'title': 'Entretien Post-Livraison', 'description': 'Après la livraison, un entretien régulier est indispensable. Nous vous accompagnons pour une sérénité au quotidien.', 'icon': 'home', 'order': 3},
                {'title': 'Nettoyage de Villas', 'description': 'Services complets de nettoyage pour villas incluant sols, murs, vitres et espaces extérieurs.', 'icon': 'home', 'order': 4},
                {'title': 'Nettoyage d\'Appartements', 'description': 'Entretien professionnel de vos appartements avec des produits de qualité et des techniques adaptées.', 'icon': 'building', 'order': 5},
                {'title': 'Nettoyage de Vitres', 'description': 'Nettoyage professionnel de toutes vos surfaces vitrées pour une transparence parfaite.', 'icon': 'sparkles', 'order': 6}
            ]
            for data in services_data:
                service = Service(**data)
                db.session.add(service)
        
        if not Testimonial.query.first():
            testimonial = Testimonial(
                name='Mohcine Tazi',
                content='Bellari a transformé notre chantier en un espace propre et accueillant. Service exceptionnel et rapide !',
                rating=5
            )
            db.session.add(testimonial)
        
        db.session.commit()

init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
