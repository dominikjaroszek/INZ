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
    status_short = db.Column(db.String(100), nullable=False)
    status_long = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)

    home_team_shots_on_goal = db.Column(db.Integer, nullable=True)
    home_team_shots_off_goal = db.Column(db.Integer, nullable=True)
    home_team_total_shots = db.Column(db.Integer, nullable=True)
    home_team_blocked_shots = db.Column(db.Integer, nullable=True)
    home_team_shots_insidebox = db.Column(db.Integer, nullable=True)
    home_team_shots_outsidebox = db.Column(db.Integer, nullable=True)
    home_team_fouls = db.Column(db.Integer, nullable=True)
    home_team_corner_kicks = db.Column(db.Integer, nullable=True)
    home_team_offsides = db.Column(db.Integer, nullable=True) 
    home_team_ball_possession = db.Column(db.Float, nullable=True)
    home_team_yellow_cards = db.Column(db.Integer, nullable=True)
    home_team_red_cards = db.Column(db.Integer, nullable=True)
    home_team_goalkeeper_saves = db.Column(db.Integer, nullable=True)
    home_team_total_passes = db.Column(db.Integer, nullable=True)
    home_team_passes_accuracy = db.Column(db.Float, nullable=True)
    home_team_passes_percent = db.Column(db.Integer, nullable=True)

    away_team_shots_on_goal = db.Column(db.Integer, nullable=True)
    away_team_shots_off_goal = db.Column(db.Integer, nullable=True)
    away_team_total_shots = db.Column(db.Integer, nullable=True)
    away_team_blocked_shots = db.Column(db.Integer, nullable=True)
    away_team_shots_insidebox = db.Column(db.Integer, nullable=True)
    away_team_shots_outsidebox = db.Column(db.Integer, nullable=True)
    away_team_fouls = db.Column(db.Integer, nullable=True)
    away_team_corner_kicks = db.Column(db.Integer, nullable=True)
    away_team_offsides = db.Column(db.Integer, nullable=True) 
    away_team_ball_possession = db.Column(db.Float, nullable=True)
    away_team_yellow_cards = db.Column(db.Integer, nullable=True)
    away_team_red_cards = db.Column(db.Integer, nullable=True)
    away_team_goalkeeper_saves = db.Column(db.Integer, nullable=True)
    away_team_total_passes = db.Column(db.Integer, nullable=True)
    away_team_passes_accuracy = db.Column(db.Float, nullable=True)
    away_team_passes_percent = db.Column(db.Integer, nullable=True)

    fans_rank_generally =  db.Column(db.Float, nullable=True)
    fans_rank_attak = db.Column(db.Float, nullable=True)
    fans_rank_defence = db.Column(db.Float, nullable=True)
    
    season = db.relationship('Season', backref=db.backref('matches', lazy=True))
    home_team = db.relationship('Team', foreign_keys=[home_team_id], backref=db.backref('home_matches', lazy=True))
    away_team = db.relationship('Team', foreign_keys=[away_team_id], backref=db.backref('away_matches', lazy=True))

    def __repr__(self):
        return f"<Match {self.home_team.name} vs {self.away_team.name}>"