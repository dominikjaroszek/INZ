from flask_sqlalchemy import SQLAlchemy
from app.config import db


class TopScorer(db.Model):
    __tablename__ = 'top_scorer'
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'), nullable=False)
    player_name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    goals = db.Column(db.Integer, nullable=False)
    assists = db.Column(db.Integer, nullable=False)

    season = db.relationship('Season', backref=db.backref('top_scorer', lazy=True))
    Team = db.relationship('Team', backref=db.backref('top_scorer', lazy=True))

    def __repr__(self):
        return f"<TopScorer {self.player_name}, Goals: {self.goals}>"