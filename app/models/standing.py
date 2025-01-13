from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Standing(db.Model):
    __tablename__ = 'standing'

    standing_id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.season_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    played = db.Column(db.Integer, nullable=False)
    win = db.Column(db.Integer, nullable=False)
    draw = db.Column(db.Integer, nullable=False)
    lose = db.Column(db.Integer, nullable=False)
    goalsFor = db.Column(db.Integer, nullable=False)
    goalsAgainst = db.Column(db.Integer, nullable=False)
    goalsDifference = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    lastUpdate = db.Column(db.DateTime, nullable=False)
    home_played = db.Column(db.Integer, nullable=False)
    home_win = db.Column(db.Integer, nullable=False)
    home_draw = db.Column(db.Integer, nullable=False)
    home_lose = db.Column(db.Integer, nullable=False)
    home_goalsFor = db.Column(db.Integer, nullable=False)
    home_goalsAgainst = db.Column(db.Integer, nullable=False)
    away_played = db.Column(db.Integer, nullable=False)
    away_win = db.Column(db.Integer, nullable=False)
    away_draw = db.Column(db.Integer, nullable=False)
    away_lose = db.Column(db.Integer, nullable=False)
    away_goalsFor = db.Column(db.Integer, nullable=False)
    away_goalsAgainst = db.Column(db.Integer, nullable=False)

    form = db.Column(db.String(100), nullable=True)
    Team = db.relationship('Team', backref='standing', lazy=True)
    Season = db.relationship('Season', backref='standing', lazy=True) 

    def __repr__(self):
        return f"<Standing Team: {self.team.name}, Position: {self.position}>"