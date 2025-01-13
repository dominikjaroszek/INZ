import pytest
from app.services.matchRatingService import get_match_rating_avg, add_match_rating, update_match_rating, delete_match_rating, get_match_rating, get_all_match_ratings
from app.models.matchRating import MatchRating
from app.models.match import Match
from app.config import db


def test_get_match_rating_avg(app, db_session):
    match_id = 1
    user_id_1 = 1
    user_id_2 = 2

    # Add ratings
    add_match_rating(match_id, user_id_1, 4)
    add_match_rating(match_id, user_id_2, 2)

    # Calculate average rating
    avg_rating = get_match_rating_avg(match_id)
    assert avg_rating == 3.0

def test_add_match_rating(app, db_session):
    match_id = 1
    user_id = 1
    rating = 4

    match_rating = add_match_rating(match_id, user_id, rating)
    assert match_rating is not None
    assert match_rating.rating == rating

def test_update_match_rating(app, db_session):
    match_id = 1
    user_id = 1
    initial_rating = 3
    updated_rating = 5

    add_match_rating(match_id, user_id, initial_rating)
    match_rating = update_match_rating(match_id, user_id, updated_rating)
    assert match_rating.rating == updated_rating

def test_delete_match_rating(app, db_session):
    match_id = 1
    user_id = 1
    rating = 4

    add_match_rating(match_id, user_id, rating)
    response = delete_match_rating(match_id, user_id)
    assert response == "Rating deleted successfully"

def test_get_match_rating(app, db_session):
    match_id = 1
    user_id = 1
    rating = 4

    add_match_rating(match_id, user_id, rating)
    match_rating = get_match_rating(match_id, user_id)
    assert match_rating is not None
    assert match_rating['rating'] == rating

def test_get_all_match_ratings(app, db_session):
    match_id = 1
    user_id_1 = 1
    user_id_2 = 2

    add_match_rating(match_id, user_id_1, 4)
    add_match_rating(match_id, user_id_2, 2)

    match_ratings = get_all_match_ratings(match_id)
    assert len(match_ratings) == 2
    assert match_ratings[0]['rating'] == 4
    assert match_ratings[1]['rating'] == 2