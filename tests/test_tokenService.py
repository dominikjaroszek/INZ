from app.services.tokenService import *

def test_get_first_free_token_id(setup_database_user):
    token_id = get_first_free_token_id()
    assert token_id == 1

def test_generate_access_token(setup_database_user):
    access_token = generate_access_token(1, "user", "Jan", "Kowalski")
    assert access_token is not None

def test_generate_refresh_token(setup_database_user):
    refresh_token = generate_refresh_token(1, "user", "Jan", "Kowalski")
    assert refresh_token is not None

def test_revoke_token(setup_database_user):
    access_token = generate_access_token(1, "user", "Jan", "Kowalski")
    refresh_token = generate_refresh_token(1, "user", "Jan", "Kowalski")
    assert revoke_token(access_token, refresh_token) == False