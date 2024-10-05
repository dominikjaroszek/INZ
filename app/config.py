from flask_sqlalchemy import SQLAlchemy

# import paypalrestsdk
# from authlib.integrations.flask_client import OAuth
# from flask_wtf.csrf import CSRFProtect
import os 
# from flask_mailman import Mail

# mail = Mail() 
db = SQLAlchemy()

# paypalrestsdk.configure({
#     "mode": "sandbox", 
#     "client_id": "AfCyxkusZA2IM5tG9K78TGlYjlMlzsKQ7G_nRP2S2BMn_920Sy8n6k7NbhsrpmpTGs14J6ECG6G4-W71",
#     "client_secret": "EGTY4q16PVR4-y9EsdAojoLruHVM7YxsI-CQvFSpvtwdOhOPBJkVI8yMg4GEZjaBnjZxNS8G2mPi8YAT"
# })

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

API_KEY = 'e1585dfda852e31d5849162cb7a24b24'
BASE_URL = 'https://v3.football.api-sports.io'