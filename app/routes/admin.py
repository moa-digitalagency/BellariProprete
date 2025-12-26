from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import Admin, Service, ContactMessage, Testimonial, SiteSettings, SEOSettings
from app.utils import generate_cleaning_image, generate_random_image

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Admin.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.dashboard'))
        flash('Identifiants incorrects', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.index'))

@admin_bp.route('/')
@login_required
def dashboard():
    unread_count = ContactMessage.query.filter_by(is_read=False).count()
    services_count = Service.query.count()
    messages_count = ContactMessage.query.count()
    testimonials_count = Testimonial.query.count()
    recent_messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         unread_count=unread_count,
                         services_count=services_count,
                         messages_count=messages_count,
                         testimonials_count=testimonials_count,
                         recent_messages=recent_messages)

@admin_bp.route('/messages')
@login_required
def messages():
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/messages/<int:id>/read', methods=['POST'])
@login_required
def mark_read(id):
    message = ContactMessage.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    return redirect(url_for('admin.messages'))

@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
def delete_message(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message supprimé', 'success')
    return redirect(url_for('admin.messages'))

@admin_bp.route('/services')
@login_required
def services():
    services = Service.query.order_by(Service.order).all()
    return render_template('admin/services.html', services=services)

@admin_bp.route('/services/add', methods=['GET', 'POST'])
@login_required
def add_service():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        long_description = request.form.get('long_description')
        icon = request.form.get('icon', 'sparkles')
        featured = request.form.get('featured') == 'on'
        order = int(request.form.get('order', 0))
        seo_title = request.form.get('seo_title')
        seo_description = request.form.get('seo_description')
        seo_keywords = request.form.get('seo_keywords')
        
        filename = f"service_{title.lower().replace(' ', '_')}.jpg"
        image_path = generate_cleaning_image(title.lower().split()[0], filename)
        
        service = Service(
            title=title, description=description, long_description=long_description,
            icon=icon, image=image_path, featured=featured, order=order,
            seo_title=seo_title, seo_description=seo_description, seo_keywords=seo_keywords
        )
        db.session.add(service)
        db.session.commit()
        flash('Service ajouté avec succès', 'success')
        return redirect(url_for('admin.services'))
    
    return render_template('admin/service_form.html', service=None)

@admin_bp.route('/services/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_service(id):
    service = Service.query.get_or_404(id)
    
    if request.method == 'POST':
        service.title = request.form.get('title')
        service.description = request.form.get('description')
        service.long_description = request.form.get('long_description')
        service.icon = request.form.get('icon')
        service.featured = request.form.get('featured') == 'on'
        service.order = int(request.form.get('order', 0))
        service.seo_title = request.form.get('seo_title')
        service.seo_description = request.form.get('seo_description')
        service.seo_keywords = request.form.get('seo_keywords')
        
        if 'image' in request.files and request.files['image']:
            filename = f"service_{service.title.lower().replace(' ', '_')}.jpg"
            image_path = generate_cleaning_image(service.title.lower().split()[0], filename)
            service.image = image_path
        
        db.session.commit()
        flash('Service modifié avec succès', 'success')
        return redirect(url_for('admin.services'))
    
    return render_template('admin/service_form.html', service=service)

@admin_bp.route('/services/<int:id>/delete', methods=['POST'])
@login_required
def delete_service(id):
    service = Service.query.get_or_404(id)
    db.session.delete(service)
    db.session.commit()
    flash('Service supprimé', 'success')
    return redirect(url_for('admin.services'))

@admin_bp.route('/testimonials')
@login_required
def testimonials():
    testimonials = Testimonial.query.all()
    return render_template('admin/testimonials.html', testimonials=testimonials)

@admin_bp.route('/testimonials/add', methods=['GET', 'POST'])
@login_required
def add_testimonial():
    if request.method == 'POST':
        name = request.form.get('name')
        content = request.form.get('content')
        rating = int(request.form.get('rating', 5))
        approved = request.form.get('approved') == 'on'
        
        testimonial = Testimonial(name=name, content=content, rating=rating, approved=approved)
        db.session.add(testimonial)
        db.session.commit()
        flash('Témoignage ajouté avec succès', 'success')
        return redirect(url_for('admin.testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=None)

@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    
    if request.method == 'POST':
        testimonial.name = request.form.get('name')
        testimonial.content = request.form.get('content')
        testimonial.rating = int(request.form.get('rating', 5))
        testimonial.approved = request.form.get('approved') == 'on'
        db.session.commit()
        flash('Témoignage modifié avec succès', 'success')
        return redirect(url_for('admin.testimonials'))
    
    return render_template('admin/testimonial_form.html', testimonial=testimonial)

@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash('Témoignage supprimé', 'success')
    return redirect(url_for('admin.testimonials'))

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = SiteSettings.query.first()
    if not settings:
        settings = SiteSettings()
        db.session.add(settings)
    
    if request.method == 'POST':
        settings.company_name = request.form.get('company_name')
        settings.phone = request.form.get('phone')
        settings.email = request.form.get('email')
        settings.whatsapp = request.form.get('whatsapp')
        settings.facebook = request.form.get('facebook')
        settings.instagram = request.form.get('instagram')
        settings.address = request.form.get('address')
        settings.logo_text = request.form.get('logo_text')
        settings.logo_color = request.form.get('logo_color', '0ea5e9')
        settings.primary_color = request.form.get('primary_color', '0ea5e9')
        settings.secondary_color = request.form.get('secondary_color', '0284c7')
        db.session.commit()
        flash('Paramètres mis à jour avec succès', 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', settings=settings)

@admin_bp.route('/seo')
@login_required
def seo():
    seo_settings = SEOSettings.query.all()
    return render_template('admin/seo.html', seo_settings=seo_settings)

@admin_bp.route('/seo/edit/<page>', methods=['GET', 'POST'])
@login_required
def edit_seo(page):
    seo = SEOSettings.query.filter_by(page_name=page).first()
    if not seo:
        seo = SEOSettings(page_name=page)
        db.session.add(seo)
    
    if request.method == 'POST':
        seo.title = request.form.get('title')
        seo.description = request.form.get('description')
        seo.keywords = request.form.get('keywords')
        seo.meta_image = request.form.get('meta_image')
        db.session.commit()
        flash('SEO mis à jour', 'success')
        return redirect(url_for('admin.seo'))
    
    return render_template('admin/seo_form.html', seo=seo)
