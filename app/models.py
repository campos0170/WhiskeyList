#models.py
from .database import db

class User(db.Model):
    id = db.Column(db.String(128), primary_key=True)  
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(129), nullable=False)

    whiskies = db.relationship('WhiskeyBottle', backref='user', lazy=True)

class WhiskeyBottle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    distillery = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    type = db.Column(db.String(100), nullable=False)
    proof = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.String(128), db.ForeignKey('user.id'), nullable=False)  
