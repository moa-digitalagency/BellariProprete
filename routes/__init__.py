import os
import uuid
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Admin, Service, ContactMessage, Testimonial, SiteSettings, SEOSettings, SiteImage
from services import ServiceManager
from utils import get_settings

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder='images'):
    if file and allowed_file(file.filename):
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4().hex}.{ext}"
        upload_path = os.path.join(current_app.static_folder, folder)
        os.makedirs(upload_path, exist_ok=True)
        file.save(os.path.join(upload_path, filename))
        return filename
    return None

def register_routes(app):
    @app.route('/')
    def index():
        featured = ServiceManager.get_featured_services()
        all_services = ServiceManager.get_all_services()
        testimonials = ServiceManager.get_approved_testimonials()
        seo = SEOSettings.query.filter_by(page_name='accueil').first()
        return render_template('public/index.html', featured_services=featured, all_services=all_services, testimonials=testimonials, seo=seo)

    @app.route('/services')
    def services():
        services = ServiceManager.get_all_services()
        seo = SEOSettings.query.filter_by(page_name='services').first()
        return render_template('public/services.html', services=services, seo=seo)

    @app.route('/service/<int:id>')
    def service_detail(id):
        service = Service.query.get_or_404(id)
        return render_template('public/service_detail.html', service=service)

    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            ServiceManager.save_message(
                name=request.form.get('name'),
                email=request.form.get('email'),
                phone=request.form.get('phone'),
                subject=request.form.get('subject'),
                message=request.form.get('message')
            )
            flash('Votre message a été envoyé avec succès!', 'success')
            return redirect(url_for('contact'))
        seo = SEOSettings.query.filter_by(page_name='contact').first()
        return render_template('public/contact.html', seo=seo)

    @app.route('/devis')
    def devis():
        seo = SEOSettings.query.filter_by(page_name='devis').first()
        return render_template('public/devis.html', seo=seo)

    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        
        if request.method == 'POST':
            user = Admin.query.filter_by(username=request.form.get('username')).first()
            if user and user.check_password(request.form.get('password')):
                login_user(user)
                return redirect(url_for('admin_dashboard'))
            flash('Identifiants incorrects', 'error')
        
        return render_template('admin/login.html')

    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        return redirect(url_for('index'))

    @app.route('/admin/')
    @login_required
    def admin_dashboard():
        unread = ContactMessage.query.filter_by(is_read=False).count()
        services = Service.query.count()
        messages = ContactMessage.query.count()
        testimonials = Testimonial.query.count()
        recent = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html',
            unread_count=unread, services_count=services,
            messages_count=messages, testimonials_count=testimonials,
            recent_messages=recent)

    @app.route('/admin/messages')
    @login_required
    def admin_messages():
        messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
        return render_template('admin/messages.html', messages=messages)

    @app.route('/admin/messages/<int:id>/read', methods=['POST'])
    @login_required
    def admin_mark_read(id):
        msg = ContactMessage.query.get_or_404(id)
        msg.is_read = True
        db.session.commit()
        return redirect(url_for('admin_messages'))

    @app.route('/admin/messages/<int:id>/delete', methods=['POST'])
    @login_required
    def admin_delete_message(id):
        msg = ContactMessage.query.get_or_404(id)
        db.session.delete(msg)
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
    def admin_add_service():
        if request.method == 'POST':
            image = 'default.jpg'
            if 'image' in request.files:
                file = request.files['image']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    image = uploaded
            
            service = Service(
                title=request.form.get('title'),
                description=request.form.get('description'),
                long_description=request.form.get('long_description'),
                icon=request.form.get('icon', 'sparkles'),
                image=image,
                featured=request.form.get('featured') == 'on',
                order=int(request.form.get('order', 0)),
                seo_title=request.form.get('seo_title'),
                seo_description=request.form.get('seo_description'),
                seo_keywords=request.form.get('seo_keywords')
            )
            db.session.add(service)
            db.session.commit()
            flash('Service ajouté avec succès', 'success')
            return redirect(url_for('admin_services'))
        return render_template('admin/service_form.html', service=None)

    @app.route('/admin/services/<int:id>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_edit_service(id):
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
            
            if 'image' in request.files:
                file = request.files['image']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    service.image = uploaded
            
            db.session.commit()
            flash('Service modifié avec succès', 'success')
            return redirect(url_for('admin_services'))
        return render_template('admin/service_form.html', service=service)

    @app.route('/admin/services/<int:id>/delete', methods=['POST'])
    @login_required
    def admin_delete_service(id):
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
    def admin_add_testimonial():
        if request.method == 'POST':
            testimonial = Testimonial(
                name=request.form.get('name'),
                content=request.form.get('content'),
                rating=int(request.form.get('rating', 5)),
                approved=request.form.get('approved') == 'on'
            )
            db.session.add(testimonial)
            db.session.commit()
            flash('Témoignage ajouté avec succès', 'success')
            return redirect(url_for('admin_testimonials'))
        return render_template('admin/testimonial_form.html', testimonial=None)

    @app.route('/admin/testimonials/<int:id>/edit', methods=['GET', 'POST'])
    @login_required
    def admin_edit_testimonial(id):
        testimonial = Testimonial.query.get_or_404(id)
        if request.method == 'POST':
            testimonial.name = request.form.get('name')
            testimonial.content = request.form.get('content')
            testimonial.rating = int(request.form.get('rating', 5))
            testimonial.approved = request.form.get('approved') == 'on'
            db.session.commit()
            flash('Témoignage modifié avec succès', 'success')
            return redirect(url_for('admin_testimonials'))
        return render_template('admin/testimonial_form.html', testimonial=testimonial)

    @app.route('/admin/testimonials/<int:id>/delete', methods=['POST'])
    @login_required
    def admin_delete_testimonial(id):
        testimonial = Testimonial.query.get_or_404(id)
        db.session.delete(testimonial)
        db.session.commit()
        flash('Témoignage supprimé', 'success')
        return redirect(url_for('admin_testimonials'))

    @app.route('/admin/settings', methods=['GET', 'POST'])
    @login_required
    def admin_settings():
        settings = SiteSettings.query.first()
        if not settings:
            settings = SiteSettings()
            db.session.add(settings)
            db.session.commit()
        
        if request.method == 'POST':
            settings.company_name = request.form.get('company_name')
            settings.phone = request.form.get('phone')
            settings.email = request.form.get('email')
            settings.whatsapp = request.form.get('whatsapp')
            settings.facebook = request.form.get('facebook')
            settings.instagram = request.form.get('instagram')
            settings.address = request.form.get('address')
            settings.logo_text = request.form.get('logo_text')
            settings.primary_color = request.form.get('primary_color', '1B4D3D')
            settings.secondary_color = request.form.get('secondary_color', '7CB342')
            settings.header_code = request.form.get('header_code', '')
            settings.footer_code = request.form.get('footer_code', '')
            settings.google_analytics = request.form.get('google_analytics', '')
            settings.google_tag_manager = request.form.get('google_tag_manager', '')
            settings.facebook_pixel = request.form.get('facebook_pixel', '')
            settings.whatsapp_default_message = request.form.get('whatsapp_default_message', '')
            settings.opening_hours = request.form.get('opening_hours', '')
            settings.map_embed = request.form.get('map_embed', '')
            
            if 'hero_image' in request.files:
                file = request.files['hero_image']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    settings.hero_image = uploaded
            
            if 'logo_image' in request.files:
                file = request.files['logo_image']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    settings.logo_image = uploaded
            
            if 'favicon' in request.files:
                file = request.files['favicon']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    settings.favicon = uploaded
            
            db.session.commit()
            flash('Paramètres mis à jour avec succès', 'success')
            return redirect(url_for('admin_settings'))
        
        return render_template('admin/settings.html', settings=settings)

    @app.route('/admin/seo')
    @login_required
    def admin_seo():
        seos = SEOSettings.query.all()
        pages = ['accueil', 'services', 'contact', 'devis']
        for page in pages:
            if not SEOSettings.query.filter_by(page_name=page).first():
                seo = SEOSettings(page_name=page, title=f'{page.capitalize()} - Bellari')
                db.session.add(seo)
        db.session.commit()
        seos = SEOSettings.query.all()
        return render_template('admin/seo.html', seo_settings=seos)

    @app.route('/admin/seo/<page>', methods=['GET', 'POST'])
    @login_required
    def admin_edit_seo(page):
        seo = SEOSettings.query.filter_by(page_name=page).first()
        if not seo:
            seo = SEOSettings(page_name=page)
            db.session.add(seo)
        
        if request.method == 'POST':
            seo.title = request.form.get('title')
            seo.description = request.form.get('description')
            seo.keywords = request.form.get('keywords')
            seo.canonical_url = request.form.get('canonical_url')
            seo.robots = request.form.get('robots', 'index, follow')
            seo.og_type = request.form.get('og_type', 'website')
            seo.twitter_card = request.form.get('twitter_card', 'summary_large_image')
            seo.structured_data = request.form.get('structured_data', '')
            seo.custom_head_code = request.form.get('custom_head_code', '')
            
            if 'meta_image' in request.files:
                file = request.files['meta_image']
                uploaded = save_uploaded_file(file)
                if uploaded:
                    seo.meta_image = uploaded
            
            db.session.commit()
            flash('SEO mis à jour', 'success')
            return redirect(url_for('admin_seo'))
        
        return render_template('admin/seo_form.html', seo=seo)

    @app.route('/admin/images')
    @login_required
    def admin_images():
        images = SiteImage.query.order_by(SiteImage.uploaded_at.desc()).all()
        return render_template('admin/images.html', images=images)

    @app.route('/admin/images/upload', methods=['POST'])
    @login_required
    def admin_upload_image():
        if 'image' not in request.files:
            flash('Aucune image sélectionnée', 'error')
            return redirect(url_for('admin_images'))
        
        file = request.files['image']
        if file.filename == '':
            flash('Aucune image sélectionnée', 'error')
            return redirect(url_for('admin_images'))
        
        uploaded = save_uploaded_file(file)
        if uploaded:
            image = SiteImage(
                name=request.form.get('name', file.filename),
                filename=uploaded,
                category=request.form.get('category', 'general'),
                alt_text=request.form.get('alt_text', '')
            )
            db.session.add(image)
            db.session.commit()
            flash('Image uploadée avec succès', 'success')
        else:
            flash('Erreur lors de l\'upload', 'error')
        
        return redirect(url_for('admin_images'))

    @app.route('/admin/images/<int:id>/delete', methods=['POST'])
    @login_required
    def admin_delete_image(id):
        image = SiteImage.query.get_or_404(id)
        try:
            filepath = os.path.join(current_app.static_folder, 'images', image.filename)
            if os.path.exists(filepath):
                os.remove(filepath)
        except:
            pass
        db.session.delete(image)
        db.session.commit()
        flash('Image supprimée', 'success')
        return redirect(url_for('admin_images'))
