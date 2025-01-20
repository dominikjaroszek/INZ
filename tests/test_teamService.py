from app.services.teamService import *
from datetime import date

def test_get_team_by_name(setup_database_match):
    team = get_team_by_name("Team A")
    assert team.team_name == "Team A"

def test_get_team(setup_database_match):
    team = get_team("Team A")
    assert team["team_name"] == "Team A"

def test_get_team_upcoming(setup_database_match):
    team = get_team_by_name("Team A")
    matches = get_team_upcoming(team, 1)
    assert len(matches) == 1

def test_get_upcoming_matches(setup_database_match):
    matches = get_upcoming_matches("Team A", 1)
    assert len(matches) == 1
    assert matches[0]["home_team"] == "Team A"
    assert matches[0]["away_team"] == "Team B"
    assert matches[0]["home_team_logo"] == "team_a_logo.png"
    assert matches[0]["away_team_logo"] == "team_b_logo.png"

def test_get_team_by_name_not_found(setup_database_match):
    team = get_team_by_name("Team K")
    assert team is None

def test_get_team_finished(setup_database_match):
    team = get_team_by_name("Team A")
    matches = get_team_finished(team, 1, 2024, 2025)
    assert len(matches) == 1
    assert matches[0].home_score == 2
    assert matches[0].away_score == 1
    assert matches[0].home_team.team_name == "Team A"
    assert matches[0].away_team.team_name == "Team D"

def test_get_team_finished_no_matches(setup_database_match):
    team = get_team_by_name("Team A")
    matches = get_team_finished(team, 1, 2020, 2021)
    assert len(matches) == 0
 
def test_get_finished_matches(setup_database_match):
    matches = get_finished_matches("Team A", 1, "2024-2025")
    assert len(matches) == 1
    assert matches[0]["home_team"] == "Team A"
    assert matches[0]["away_team"] == "Team D"
    assert matches[0]["home_score"] == 2
    assert matches[0]["away_score"] == 1
    assert matches[0]["home_team_logo"] == "team_a_logo.png"
    assert matches[0]["away_team_logo"] == "team_d_logo.png"

def test_search_team(setup_database_match):
    teams = search_team("Team")
    assert len(teams) == 6
    assert teams[0]["name"] == "Team A"
    assert teams[1]["name"] == "Team B"
    assert teams[2]["name"] == "Team C"
    assert teams[3]["name"] == "Team D"
    team = search_team("A")
    assert len(team) == 8