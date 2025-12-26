from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, Admin, Service, ContactMessage, Testimonial, SiteSettings, SEOSettings
from services import ServiceManager
from utils import generate_random_image, get_settings

def register_routes(app):
    @app.route('/')
    def index():
        featured = ServiceManager.get_featured_services()
        all_services = ServiceManager.get_all_services()
        testimonials = ServiceManager.get_approved_testimonials()
        return render_template('public/index.html', featured_services=featured, all_services=all_services, testimonials=testimonials)

    @app.route('/services')
    def services():
        services = ServiceManager.get_all_services()
        return render_template('public/services.html', services=services)

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
        return render_template('public/contact.html')

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
            image = generate_random_image(filename=f"service_{request.form.get('title').lower().replace(' ', '_')}.jpg")
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
        
        if request.method == 'POST':
            settings.company_name = request.form.get('company_name')
            settings.phone = request.form.get('phone')
            settings.email = request.form.get('email')
            settings.whatsapp = request.form.get('whatsapp')
            settings.facebook = request.form.get('facebook')
            settings.instagram = request.form.get('instagram')
            settings.address = request.form.get('address')
            settings.logo_text = request.form.get('logo_text')
            db.session.commit()
            flash('Paramètres mis à jour avec succès', 'success')
            return redirect(url_for('admin_settings'))
        
        return render_template('admin/settings.html', settings=settings)

    @app.route('/admin/seo')
    @login_required
    def admin_seo():
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
            db.session.commit()
            flash('SEO mis à jour', 'success')
            return redirect(url_for('admin_seo'))
        
        return render_template('admin/seo_form.html', seo=seo)
