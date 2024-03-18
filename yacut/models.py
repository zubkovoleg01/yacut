from datetime import datetime

from yacut import db

class URL_map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(180), nullable=False)
    short = db.Column(db.String(180))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)