from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Service, Testimonial
from app.services import ServiceManager
from app.utils import get_settings

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    featured_services = ServiceManager.get_featured_services()
    all_services = ServiceManager.get_all_services()
    testimonials = ServiceManager.get_approved_testimonials()
    settings = get_settings()
    return render_template('public/index.html', 
                         featured_services=featured_services,
                         all_services=all_services,
                         testimonials=testimonials,
                         settings=settings)

@public_bp.route('/services')
def services():
    services = ServiceManager.get_all_services()
    settings = get_settings()
    return render_template('public/services.html', services=services, settings=settings)

@public_bp.route('/service/<int:id>')
def service_detail(id):
    service = Service.query.get_or_404(id)
    settings = get_settings()
    return render_template('public/service_detail.html', service=service, settings=settings)

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    settings = get_settings()
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        ServiceManager.save_message(name, email, phone, subject, message)
        flash('Votre message a été envoyé avec succès!', 'success')
        return redirect(url_for('public.contact'))
    
    return render_template('public/contact.html', settings=settings)
