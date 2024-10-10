from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Match(db.Model):
    __tablename__ = 'match'
    match_id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'), nullable=False)
    home_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    away_team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    home_score = db.Column(db.Integer, nullable=True)
    away_score = db.Column(db.Integer, nullable=True)
    referee = db.Column(db.String(100), nullable=True)
    match_date = db.Column(db.DateTime, nullable=False)
    venue_name = db.Column(db.String(100), nullable=False)
    round = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)

    
    season = db.relationship('Season', backref=db.backref('matches', lazy=True))
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref=db.backref('home_matches', lazy=True))
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref=db.backref('away_matches', lazy=True))

    def __repr__(self):
        return f"<Match {self.home_team.name} vs {self.away_team.name}>"