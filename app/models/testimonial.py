from app import db

class Testimonial(db.Model):
    __tablename__ = 'testimonial'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image = db.Column(db.String(255))
    approved = db.Column(db.Boolean, default=False)
