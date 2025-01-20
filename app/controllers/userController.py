from flask import Blueprint, request, jsonify, session
from app.config import db
from app.schemas.user_schema import UserRegistrationModel, UserLoginModel, UserUpdate
from pydantic import ValidationError
from app.services.userService import *
from app.services.tokenService import *
from sqlalchemy import update
from app.decorators import *

user_bp = Blueprint('user_bp', __name__)

@user_bp.route("/register", methods=["POST"])
def register_user():
    try:
        data = UserRegistrationModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    if get_user_by_email(data.email):
        return jsonify({"message": "Email already exists"}), 400

    try:
        create_user(
            firstName=data.firstName,
            lastName=data.lastName,
            email=data.email,
            password=data.password,
        )
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = UserLoginModel(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    user = get_user_by_email(data.email)
    if check_password_controller(user, data.password):
        
        access_token = generate_access_token(user.user_id, user.role.name, user.firstName, user.lastName)
        refresh_token = generate_refresh_token(user.user_id, user.role.name, user.firstName, user.lastName)
        token = Token(token_id = get_first_free_token_id(), refresh_token = refresh_token, access_token = access_token, user_id = user.user_id )
        db.session.add(token)
        db.session.commit()
        return jsonify({'access_token': access_token, 'refresh_token': refresh_token}), 200
    
    return jsonify({'message': 'Nieprawidłowe dane logowania'}), 401


@user_bp.route('/logout', methods=['DELETE'])
def logout():
    access_token = None
    if 'x-access-tokens' in request.headers:
        access_token = request.headers['x-access-tokens']
    print(access_token)

    refresh_token = None    
    if 'x-refresh-tokens' in request.headers:
        refresh_token = request.headers['x-refresh-tokens']
    print(refresh_token)

    if revoke_token(access_token, refresh_token):
        return jsonify({"message": "Refresh and aceess token revoked"}),200
    
    
    return jsonify({"message": "Invalid refresh token"}), 400
    

@user_bp.route('/contact', methods=['GET'])
@token_required
@role_required('user')
def get_contact(current_user):
    user = get_user_by_id(current_user.user_id)
    return jsonify(user.to_json_user())


@user_bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.headers.get('x-refresh-tokens')
    
    if not refresh_token:
        return jsonify({'message': 'Refresh token is missing'}), 400
    
    try:
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Refresh token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid refresh token'}), 401
    
    current_user = User.query.filter_by(user_id=data['user_id']).first()
    if current_user is None:
        return jsonify({'message': 'Invalid refresh token'}), 401
    
    stored_token = Token.query.filter_by(refresh_token=refresh_token).first()
    if not stored_token:
        return jsonify({'message': 'Invalid or expired refresh token'}), 401
    
    new_access_token = generate_access_token(current_user.user_id, current_user.role.name, current_user.firstName, current_user.lastName)

    stmt = update(Token).where(Token.token_id == stored_token.token_id).values(access_token=new_access_token)
    db.session.execute(stmt)
    db.session.commit()
    return jsonify({'access_token': new_access_token})

@user_bp.route('/user/change_password', methods=['PATCH'])
@token_required
@role_required('user')
def change_password_controller(current_user):
    try:
        data = UserUpdate(**request.json)
    except ValidationError as e:
        return jsonify({"message": e.errors()}), 400

    user = get_user_by_id(current_user.user_id)
    if not check_password_controller(user, data.oldPassword):
        return jsonify({'message': 'Wrong password'}), 401

    if data.oldPassword == data.newPassword:
        return jsonify({'message': 'The new password must be used over the old one'}), 400

    change_password(data, user )
    return jsonify({'message': 'Password changed successfully'}), 200