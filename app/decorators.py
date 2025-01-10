import jwt
from functools import wraps
from flask import request, jsonify, current_app
from app.models.user import User

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
           token = request.headers['x-access-tokens']
 
        if not token:
           return jsonify({'message': 'a valid token is missing'}), 401


        try:
           data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
           print(data)
           current_user = User.query.filter_by(user_id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
           return jsonify({'message': 'token has expired'}), 401
        except jwt.InvalidTokenError:
           return jsonify({'message': 'token is invalid'}), 401
 
        return f(current_user, *args, **kwargs)
   return decorator




def role_required(role_name):
    def decorator(func):
        @wraps(func)
        def authorize(current_user, *args, **kwargs):
            print(current_user.role.name)
            role = current_user.role.name
            if role_name not in role:
                return jsonify({'message': 'role is invalid. You need to be ' +str(role_name) +'to access this route'})
            return func(current_user, *args, **kwargs)
        return authorize
    return decorator
