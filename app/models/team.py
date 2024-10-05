from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    nameTeam = db.Column(db.String(100), nullable=False)
    league_id = db.Column(db.Integer, db.ForeignKey('league.id'), nullable=False)

    league = db.relationship('League', backref=db.backref('teams', lazy=True))

    def __repr__(self):
        return f"<Team {self.nameTeam}>"