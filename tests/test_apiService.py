from app.services.apiService import *
from app.services.matchService import *
import pytest

# def test_oblicz_faule(setup_database_match):
#     match = get_match_by_id_data(1)
#     assert oblicz_faule(match) == 22

# def test_oblicz_zolte_kartki(setup_database_match):
#     match = get_match_by_id_data(1)
#     assert oblicz_zolte_kartki(match) == 3

# def test_oblicz_czerwone_kartki(setup_database_match):
#     match = get_match_by_id_data(1)
#     assert oblicz_czerwone_kartki(match) == 0

# def test_oblicz_wskaznik_agresji(setup_database_match):
#     match = get_match_by_id_data(16)
#     assert oblicz_wskaznik_agresji(match) == 80.41

class Match:
    def __init__(self, home_score=None, away_score=None, home_team_ball_possession=None, 
                 away_team_ball_possession=None, home_team_corner_kicks=None, 
                 away_team_corner_kicks=None, home_team_total_shots=None, away_team_total_shots=None,
                 home_team_offsides=None, away_team_offsides=None):
        self.home_score = home_score
        self.away_score = away_score
        self.home_team_ball_possession = home_team_ball_possession
        self.away_team_ball_possession = away_team_ball_possession
        self.home_team_corner_kicks = home_team_corner_kicks
        self.away_team_corner_kicks = away_team_corner_kicks
        self.home_team_total_shots = home_team_total_shots
        self.away_team_total_shots = away_team_total_shots
        self.home_team_offsides = home_team_offsides  
        self.away_team_offsides = away_team_offsides 

class Standing:
    def __init__(self, form=None):
        self.form = form

@pytest.fixture
def mock_data():
    return [
        Match(home_score=2, away_score=1, home_team_ball_possession=60, home_team_corner_kicks=5, away_team_corner_kicks=3,
              home_team_total_shots=15, away_team_total_shots=10, home_team_offsides=2, away_team_offsides=1),
        Match(home_score=3, away_score=2, home_team_ball_possession=65, home_team_corner_kicks=6, away_team_corner_kicks=4,
              home_team_total_shots=18, away_team_total_shots=12, home_team_offsides=3, away_team_offsides=2),
        Match(home_score=1, away_score=1, home_team_ball_possession=55, home_team_corner_kicks=3, away_team_corner_kicks=2,
              home_team_total_shots=10, away_team_total_shots=8, home_team_offsides=1, away_team_offsides=1),
        Match(home_score=0, away_score=0, home_team_ball_possession=50, home_team_corner_kicks=2, away_team_corner_kicks=2,
              home_team_total_shots=5, away_team_total_shots=6, home_team_offsides=0, away_team_offsides=0),
        Match(home_score=4, away_score=3, home_team_ball_possession=70, home_team_corner_kicks=7, away_team_corner_kicks=5,
              home_team_total_shots=20, away_team_total_shots=15, home_team_offsides=4, away_team_offsides=3),
    ]


@pytest.fixture
def mock_standing():
    # Mockowanie formy drużyny
    return Standing(form="WWDDL")  # 3 zwycięstwa, 2 remisy

@pytest.fixture
def mock_standing_zero():
    # Mockowanie formy drużyny
    return Standing(form="LLLLL")  # 3 zwycięstwa, 2 remisy

# Testowanie obliczania formy drużyny
def test_oblicz_form(mock_standing):
    result = oblicz_form(mock_standing)
    expected_result = 8  # 3*3 (zwycięstwa) + 2*1 (remisy)
    assert result == expected_result

def test_oblicz_form(mock_standing_zero):
    result = oblicz_form(mock_standing_zero)
    expected_result = 0  # 3*3 (zwycięstwa) + 2*1 (remisy)
    assert result == expected_result

# Testowanie obliczania ofensywy drużyny
def test_oblicz_ofensywa(mock_data):
    result = oblicz_ofensywa(mock_data)
    expected_result = 17  # 2+1 + 3+2 + 1+1 + 0+0 + 4+3
    assert result == expected_result

# Testowanie obliczania obrony drużyny
def test_oblicz_obrona(mock_data):
    result = oblicz_obrona(mock_data)
    expected_result = 17  # 1+2 + 2+3 + 1+1 + 0+0 + 3+4
    assert result == expected_result


# Test dla obliczania statystyk drużyny
def test_oblicz_statystyki_bramkoszczelnosci(mock_data):
    result = oblicz_statystyki_bramkoszczelnosci(mock_data)
    
    # Sprawdzamy, czy wynik mieści się w oczekiwanym zakresie
    assert result >= 0
    assert result <= 100


# Test normalizacji statystyk
def test_znormalizuj_wg_bramkoszczelnosci():
    values = {
        "possession": 60,
        "corners": 5,
        "goals": 3,
        "shots": 10,
        "penalties": 2,
    }
    max_values = {
        "possession": 350,  # 70 * 5
        "corners": 50,      # 10 * 5
        "goals": 25,        # 5 * 5
        "shots": 100,       # 20 * 5
        "penalties": 50,    # 10 * 5
    }
    
    result = znormalizuj_wg_bramkoszczelnosci(values, max_values)
    assert 0 <= result <= 100


# Test dla obliczania średniej ważonej
def test_wylicz_srednia_wazona():
    wg_team1 = 80
    wg_team2 = 60
    waga_team1 = 0.6
    waga_team2 = 0.4

    result = wylicz_srednia_wazona(wg_team1, wg_team2, waga_team1, waga_team2)
    
    # Obliczamy średnią ważoną ręcznie
    expected_result = (wg_team1 * waga_team1 + wg_team2 * waga_team2) / (waga_team1 + waga_team2)
    
    assert result == expected_result


