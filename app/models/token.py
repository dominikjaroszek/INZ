from app.config import db

class Token(db.Model):
    token_id = db.Column(db.Integer, primary_key=True)
    refresh_token = db.Column(db.String(512), nullable=False, unique=True)
    access_token = db.Column(db.String(512), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)