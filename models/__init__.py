from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

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
    long_description = db.Column(db.Text)
    icon = db.Column(db.String(50), default='sparkles')
    image = db.Column(db.String(255), default='default.jpg')
    featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    seo_title = db.Column(db.String(200))
    seo_description = db.Column(db.String(500))
    seo_keywords = db.Column(db.String(500))

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)

class SiteSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='Bellari Propreté Services')
    phone = db.Column(db.String(30), default='+212 6 80 76 03 52')
    email = db.Column(db.String(120), default='bellari.groupe@gmail.com')
    whatsapp = db.Column(db.String(30), default='+212680760352')
    facebook = db.Column(db.String(200), default='')
    instagram = db.Column(db.String(200), default='')
    address = db.Column(db.Text, default='Maroc')
    logo_text = db.Column(db.String(100), default='Bellari')
    primary_color = db.Column(db.String(10), default='1B4D3D')
    secondary_color = db.Column(db.String(10), default='7CB342')
    hero_image = db.Column(db.String(255), default='cleaning_team_at_work.png')
    about_image = db.Column(db.String(255), default='clean_office_space.png')
    logo_image = db.Column(db.String(255), default='')
    favicon = db.Column(db.String(255), default='')
    header_code = db.Column(db.Text, default='')
    footer_code = db.Column(db.Text, default='')
    google_analytics = db.Column(db.String(50), default='')
    google_tag_manager = db.Column(db.String(50), default='')
    facebook_pixel = db.Column(db.String(50), default='')
    whatsapp_default_message = db.Column(db.Text, default='Bonjour, je souhaite demander un devis pour vos services de nettoyage.')
    opening_hours = db.Column(db.String(200), default='Lun-Sam: 8h-18h')
    map_embed = db.Column(db.Text, default='')

class SEOSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    keywords = db.Column(db.String(500))
    meta_image = db.Column(db.String(255))
    canonical_url = db.Column(db.String(255))
    robots = db.Column(db.String(100), default='index, follow')
    og_type = db.Column(db.String(50), default='website')
    twitter_card = db.Column(db.String(50), default='summary_large_image')
    structured_data = db.Column(db.Text, default='')
    custom_head_code = db.Column(db.Text, default='')

class SiteImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(50), default='general')
    alt_text = db.Column(db.String(200))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
