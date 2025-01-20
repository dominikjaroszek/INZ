import os
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from .config import db
from .controllers.leagueController import league_bp
from .controllers.matchController import match_bp
from .controllers.fetchController import fetch_bp
from .controllers.standingController import standing_bp
from .controllers.topScorerController import topScorer_bp
from .controllers.teamController import team_bp
from .controllers.userController import user_bp
from .controllers.matchRatingController import matchRating_bp
from .controllers.apiController import api_bp


def create_app(baza):
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = baza
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    access_token_expires_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES', 5))
    refresh_token_expires_days = int(os.getenv('REFRESH_TOKEN_EXPIRES_DAYS', 7))

    app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=access_token_expires_minutes)
    app.config['REFRESH_TOKEN_EXPIRES'] = timedelta(days=refresh_token_expires_days)

    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
    
    app.register_blueprint(league_bp)
    app.register_blueprint(match_bp)
    app.register_blueprint(fetch_bp)
    app.register_blueprint(standing_bp)
    app.register_blueprint(topScorer_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(matchRating_bp)
    app.register_blueprint(api_bp)
    

    db.init_app(app)
    return app