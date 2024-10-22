from flask_sqlalchemy import SQLAlchemy
from app.config import db


class Season(db.Model):
    __tablename__ = 'season'
    season_id = db.Column(db.Integer, primary_key=True)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    is_current = db.Column(db.Boolean, nullable=False)

    league = db.relationship('League', backref=db.backref('season', lazy=True))

    def __repr__(self):
        return f"<Season {self.start_year}/{self.end_year}>"
    
