from app.models import Service, ContactMessage, Testimonial, SiteSettings
from app import db

class ServiceManager:
    @staticmethod
    def get_featured_services():
        return Service.query.filter_by(featured=True).order_by(Service.order).all()
    
    @staticmethod
    def get_all_services():
        return Service.query.order_by(Service.order).all()
    
    @staticmethod
    def get_recent_messages(limit=5):
        return ContactMessage.query.filter_by(is_read=False).order_by(ContactMessage.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_approved_testimonials():
        return Testimonial.query.filter_by(approved=True).all()
    
    @staticmethod
    def save_message(name, email, phone, subject, message):
        msg = ContactMessage(name=name, email=email, phone=phone, subject=subject, message=message)
        db.session.add(msg)
        db.session.commit()
        return msg
