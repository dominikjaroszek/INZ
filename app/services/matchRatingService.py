from app.models.matchRating import MatchRating
from app.models.match import Match
from app.config import db

def get_all_match_ratings(match_id):
    match_ratings = Match.query.filter_by(match_id=match_id).first().ratings

    return [rating.to_json() for rating in match_ratings]

def get_match_rating(match_id, user_id):
    match_rating = MatchRating.query.filter_by(match_id=match_id, user_id=user_id).first()
    if match_rating is None:
        return None
    return match_rating.to_json()

def add_match_rating(match_id, user_id, rating ):
    if rating < 0 or rating > 5:
        return None
    
    match_rating = MatchRating(match_id=match_id, user_id=user_id, rating=rating)
    db.session.add(match_rating)
    db.session.commit()
    return match_rating

def update_match_rating(match_id, user_id, rating):
    match_rating = MatchRating.query.filter_by(match_id=match_id, user_id=user_id).first()
    match_rating.rating = rating
    db.session.commit()
    return match_rating

def delete_match_rating(match_id, user_id):
    match_rating = MatchRating.query.filter_by(match_id=match_id, user_id=user_id).first()
    db.session.delete(match_rating)
    db.session.commit()
    return "Rating deleted successfully"

def get_match_rating_avg(match_id):
    match_ratings = Match.query.filter_by(match_id=match_id).first().ratings
    match_ratings_sum = sum([rating.rating for rating in match_ratings])
    match_ratings_count = len(match_ratings)
    return match_ratings_sum / match_ratings_count

