from flask_sqlalchemy import SQLAlchemy
import os 

db = SQLAlchemy()


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

API_KEY = 'e1585dfda852e31d5849162cb7a24b24'
BASE_URL = 'https://v3.football.api-sports.io/'

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "https://v3.football.api-sports.io"
}

ACCESS_TOKEN_EXPIRES = 5
REFRESH_TOKEN_EXPIRES = 7