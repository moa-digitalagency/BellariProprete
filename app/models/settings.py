from app import db

class SiteSettings(db.Model):
    __tablename__ = 'site_settings'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), default='Bellari Propreté Services')
    phone = db.Column(db.String(30), default='+212 6 80 76 03 52')
    email = db.Column(db.String(120), default='bellari.groupe@gmail.com')
    whatsapp = db.Column(db.String(30), default='+33774496440')
    facebook = db.Column(db.String(200), default='https://www.facebook.com/profile.php?id=61579236225216')
    instagram = db.Column(db.String(200), default='https://www.instagram.com/shabakainvest/')
    address = db.Column(db.Text, default='Maroc')
    logo_text = db.Column(db.String(100), default='Bellari')
    logo_color = db.Column(db.String(10), default='0ea5e9')
    primary_color = db.Column(db.String(10), default='0ea5e9')
    secondary_color = db.Column(db.String(10), default='0284c7')

class SEOSettings(db.Model):
    __tablename__ = 'seo_settings'
    id = db.Column(db.Integer, primary_key=True)
    page_name = db.Column(db.String(100), unique=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(500))
    keywords = db.Column(db.String(500))
    meta_image = db.Column(db.String(255))
