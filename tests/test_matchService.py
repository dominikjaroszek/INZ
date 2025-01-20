from app.services.matchService import *
from app.models.match import Match
from app.controllers.matchController import *

def test_get_match_by_id_data(setup_database_match):
    match = get_match_by_id_data(1)
    if match is None:
        assert False
    else:
        assert True

def test_next_round_league(setup_database_match):
    next_round = next_round_league(1)  # Liga 1 (Premier League)
    assert next_round == "Round 20"  # Spodziewana najbliższa runda

def test_finished_last_match(setup_database_match):
    matches = finished_last_match(1, 2024, 2025, 5)  # Team A, sezon 2024-2025
    assert len(matches) == 5  # Spodziewana liczba meczów
    assert all(match.type == "Finished" for match in matches)

def test_get_upcoming_matches_by_round(setup_database_match):
    upcoming_matches = get_upcoming_matches_by_round(1, "Round 20")  # Liga 1, runda 20
    assert len(upcoming_matches) == 1  # Spodziewany 1 mecz
    assert upcoming_matches[0].round == "Round 20"

def test_get_upcoming_rounds(setup_database_match):
    upcoming_rounds = get_upcoming_rounds()
    assert len(upcoming_rounds) == 2  # Dwie ligi
    for league in upcoming_rounds:
        assert "matches" in league
        assert len(league["matches"]) > 0  # Spodziewane mecze w każdej lidze

def test_get_upcoming_rounds_fans(setup_database_match):
    upcoming_rounds = get_upcoming_rounds_fans()
    assert len(upcoming_rounds) == 2  # Dwie ligi
    for league in upcoming_rounds:
        assert "matches" in league
        for match in league["matches"]:
            assert "fans_rank_generally" in match
            assert "fans_rank_attak" in match
            assert "fans_rank_defence" in match

def test_get_match_by_id(setup_database_match):
    match = get_match_by_id(1)
    assert match['match_id'] == 1 
