from flask_sqlalchemy import SQLAlchemy
from app.config import db

class Standing(db.Model):
    __tablename__ = 'standing'

    standing_id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    Played = db.Column(db.Integer, nullable=False)
    Win = db.Column(db.Integer, nullable=False)
    Draw = db.Column(db.Integer, nullable=False)
    Lose = db.Column(db.Integer, nullable=False)



    GoalsFor = db.Column(db.Integer, nullable=False)
    GoalsAgainst = db.Column(db.Integer, nullable=False)
    GoalsDifference = db.Column(db.Integer, nullable=False)
    Form = db.Column(db.String(100), nullable=False)
    Status = db.Column(db.String(100), nullable=False)
    LastUpdate = db.Column(db.String(100), nullable=False)
    Team = db.relationship('Team', backref='standing', lazy=True)
    League = db.relationship('League', backref='standing', lazy=True)
    Season = db.relationship('Season', backref='standing', lazy=True) 

    def __repr__(self):
        return f"<Standing Team: {self.team.name}, Position: {self.position}>"