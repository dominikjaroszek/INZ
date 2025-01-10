from flask import Blueprint, jsonify, abort, request
from app.services.matchRatingService import *
from app.decorators import *
matchRating_bp = Blueprint('matchRating_bp', __name__)

@matchRating_bp.route('/matchRating/<int:match_id>', methods=['GET'])
def get_all_match_ratings_route(match_id):
    match_ratings = get_all_match_ratings(match_id)
    return jsonify(match_ratings)


@matchRating_bp.route('/matchRating/user/<int:match_id>', methods=['GET'])
@token_required
@role_required('user')
def get_match_rating_route(current_user, match_id,):
    match_rating = get_match_rating(match_id, current_user.user_id)
    if match_rating is None:
        return jsonify({})
    return jsonify(match_rating)


@matchRating_bp.route('/matchRating', methods=['POST'])
@token_required
@role_required('user')
def add_match_rating_route(current_user):
    match_id = request.json['match_id']
    rating = request.json['rating']
    match_rating = add_match_rating(match_id, current_user.user_id, rating)
    if match_rating is None:
        abort(400, 'Rating must be between 0 and 5')
    return jsonify({"message": 'Rating added successfully'})

@matchRating_bp.route('/matchRating', methods=['PATCH'])
@token_required
@role_required('user')
def update_match_rating_route(current_user):
    match_id = request.json['match_id']
    rating = request.json['rating']
    match_rating = update_match_rating(match_id, current_user.user_id, rating)
    if match_rating is None:
        abort(400, 'Rating must be between 0 and 5')
    return jsonify({"message": 'Rating added successfully'})

@matchRating_bp.route('/matchRating/user/<int:match_id>', methods=['DELETE'])
@token_required
@role_required('user')
def delete_match_rating_route(current_user, match_id):
        match_rating = delete_match_rating(match_id, current_user.user_id)
        return jsonify({"message": match_rating})

@matchRating_bp.route('/matchRating/avg/<int:match_id>', methods=['GET'])
def get_match_rating_avg_route(match_id):
        match_rating_avg = get_match_rating_avg(match_id)
        return jsonify(match_rating_avg)

