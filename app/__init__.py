import os
from flask import Flask
from datetime import timedelta
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .config import db
# from .services.userService import userbp
# from .services.ticketService import ticketbp
# from .services.privilageService import privilagebp
# from .services.planeService import planebp
# from .services.paymentService import paymentbp
# from .services.orderService import orderbp
# from .services.googleService import googlebp
# from .services.followService import followbp
# from .services.flightService import fligtbp
# from .services.airportService import airportbp
from .controllers.leagueController import leaguebp
# from .services.roleService import rolebp

def create_app():
    app = Flask(__name__)

    # Use environment variables for configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # access_token_expires_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES', 5))
    # refresh_token_expires_days = int(os.getenv('REFRESH_TOKEN_EXPIRES_DAYS', 7))

    # app.config['ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=access_token_expires_minutes)
    # app.config['REFRESH_TOKEN_EXPIRES'] = timedelta(days=refresh_token_expires_days)

    # app.config['BLACKLIST'] = set()
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
    
    # app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    # app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
 

    # app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    # app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'False') == 'True'
    # app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL', 'True') == 'True'

    # app.register_blueprint(userbp)
    # app.register_blueprint(ticketbp)
    # app.register_blueprint(privilagebp)
    # app.register_blueprint(planebp)
    # app.register_blueprint(paymentbp)
    # app.register_blueprint(orderbp)
    # app.register_blueprint(googlebp)
    # app.register_blueprint(followbp)
    # app.register_blueprint(fligtbp)
    # app.register_blueprint(airportbp)
    app.register_blueprint(leaguebp)
    # app.register_blueprint(rolebp)

    db.init_app(app)
    # mail.init_app(app)
    return app