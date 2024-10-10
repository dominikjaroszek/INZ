from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.league_id'), nullable=False)
    logo = db.Column(db.String(100), nullable=False)
    venue_name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    founded = db.Column(db.Integer, nullable=False)
    league = db.relationship('League', backref=db.backref('teams', lazy=True))

    def __repr__(self):
        return f"<Team {self.nameTeam}>"