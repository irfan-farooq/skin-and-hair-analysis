
from app.extensions import db
from datetime import datetime
class User(db.Model):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String, nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.utcnow)
class Scan(db.Model):
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    user_id=db.Column(db.String,db.ForeignKey('user.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    skin_tone = db.Column(db.String)
    undertone = db.Column(db.String)
    acne_severity = db.Column(db.String)
    acne_zones = db.Column(db.String)
    face_shape = db.Column(db.String)
    hair_type = db.Column(db.String)
    eye_color = db.Column(db.String)
    lip_color = db.Column(db.String)    
    health_score = db.Column(db.Float)
    advice_json = db.Column(db.Text)
    dark_circles = db.Column(db.String)
    skin_hex = db.Column(db.String)
    lip_hex = db.Column(db.String)