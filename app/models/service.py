from app import db

class Service(db.Model):
    __tablename__ = 'service'
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
