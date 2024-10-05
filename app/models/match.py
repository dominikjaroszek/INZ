from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Match(db.Model):
    __tablename__ = 'match'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    home_score = db.Column(db.Integer, nullable=False)
    away_score = db.Column(db.Integer, nullable=False)

    season = db.relationship('Season', backref=db.backref('matches', lazy=True))
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref=db.backref('home_matches', lazy=True))
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref=db.backref('away_matches', lazy=True))

    def __repr__(self):
        return f"<Match {self.home_team.name} vs {self.away_team.name}>"