from flask_sqlalchemy import SQLAlchemy
from app.config import db


class TopScorer(db.Model):
    __tablename__ = 'top_scorer'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    player_name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    goals = db.Column(db.Integer, nullable=False)

    season = db.relationship('Season', backref=db.backref('top_scorers', lazy=True))
    team = db.relationship('Team', backref=db.backref('top_scorers', lazy=True))

    def __repr__(self):
        return f"<TopScorer {self.player_name}, Goals: {self.goals}>"