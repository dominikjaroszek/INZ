from app.config import db
from app.models.token import Token
from flask import request, jsonify, current_app
from datetime import datetime, timedelta
import jwt


def get_first_free_token_id():
    all_token_ids = db.session.query(Token.token_id).order_by(Token.token_id).all()
    all_token_ids = [row.token_id for row in all_token_ids]
    
    for index in range(1, len(all_token_ids) + 1):
        if index not in all_token_ids:
            return index
    
    return len(all_token_ids) + 1

def generate_access_token(user_id, role, firstName, lastName):
    payload = {
        'exp': datetime.utcnow() + current_app.config['ACCESS_TOKEN_EXPIRES'],
        'iat': datetime.utcnow(),
        'user_id': user_id,
        'role': role,
        'firstName': firstName,
        'lastName': lastName

    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def generate_refresh_token(user_id, role, firstName, lastName):
    payload = {
        'exp': datetime.utcnow() + current_app.config['REFRESH_TOKEN_EXPIRES'],
        'iat': datetime.utcnow(),
        'user_id': user_id,
        'role': role,
        'firstName': firstName,
        'lastName': lastName
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def revoke_token(access_token, refresh_token):
    token = Token.query.filter_by(refresh_token=refresh_token, access_token=access_token).first()
    if  token:
        db.session.delete(token)
        db.session.commit()
        return True
    return False