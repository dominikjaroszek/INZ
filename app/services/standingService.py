from app.models.standing import Standing
from app.models.league import League
from app.models.season import Season
from app.config import db

def get_standings(league_name, season):
    season_start_year = season.split('-')[0]

    league = db.session.query(League).filter_by(league_name=league_name).first()
    season = db.session.query(Season).filter_by(league_id=league.league_id, start_year=season_start_year).first()

    if not league or not season:
        return {'error': 'League or season not found'}

    standings = db.session.query(Standing).filter_by(season_id=season.season_id).order_by(Standing.position).all()
    standings_data = []

    for standing in standings:
        standings_data.append({
            "position": standing.position,
            "team_name": standing.Team.team_name,
            "played": standing.played,
            "win": standing.win,
            "draw": standing.draw,
            "lose": standing.lose,
            "goalsFor": standing.goalsFor,
            "goalsAgainst": standing.goalsAgainst,
            "goalDifference": standing.goalsDifference,
            "points": standing.points,
            "status": standing.status,
            "form" : standing.form[-5:][::-1],  # Get the last 5 characters from form
        })


    return standings_data


def get_standings_home(league_name, season):
    # Wyciągnięcie roku początkowego sezonu
    season_start_year = season.split('-')[0]

    # Wyszukiwanie ligi i sezonu w bazie danych
    league = db.session.query(League).filter_by(league_name=league_name).first()
    season = db.session.query(Season).filter_by(league_id=league.league_id, start_year=season_start_year).first()

    # Sprawdzanie, czy liga i sezon istnieją
    if not league or not season:
        return {'error': 'League or season not found'}

    # Pobieranie tabeli ligowej
    standings = db.session.query(Standing).filter_by(season_id=season.season_id).order_by(Standing.position).all()
    standings_data = []

    # Tworzenie listy wyników
    for standing in standings:
        standings_data.append({
            "team_name": standing.Team.team_name,
            "played": standing.home_played,
            "win": standing.home_win,
            "draw": standing.home_draw,
            "lose": standing.home_lose,
            "goalsFor": standing.home_goalsFor,
            "goalsAgainst": standing.home_goalsAgainst,
            "goalDifference": standing.home_goalsFor-standing.home_goalsAgainst,
            "points": standing.home_win * 3 + standing.home_draw, 
        })

    # Sortowanie drużyn na podstawie punktów (od najwyższej do najniższej)
    standings_data.sort(key=lambda x: (x['points'], x['goalDifference']), reverse=True)

    # Przypisywanie pozycji w tabeli
    for index, team in enumerate(standings_data, start=1):
        team['position'] = index

    return standings_data


def get_standings_away(league_name, season):
    season_start_year = season.split('-')[0]

    league = db.session.query(League).filter_by(league_name=league_name).first()
    season = db.session.query(Season).filter_by(league_id=league.league_id, start_year=season_start_year).first()

    if not league or not season:
        return {'error': 'League or season not found'}

    standings = db.session.query(Standing).filter_by(season_id=season.season_id).order_by(Standing.position).all()
    standings_data = []

    for standing in standings:
        standings_data.append({
            "team_name": standing.Team.team_name,
            "played": standing.away_played,
            "win": standing.away_win,
            "draw": standing.away_draw,
            "lose": standing.away_lose,
            "goalsFor": standing.away_goalsFor,
            "goalsAgainst": standing.away_goalsAgainst,
            "goalDifference": standing.away_goalsFor-standing.away_goalsAgainst,
            "points": standing.away_win * 3 + standing.away_draw, 
        })

    standings_data.sort(key=lambda x: (x['points'], x['goalDifference']), reverse=True)

    for index, team in enumerate(standings_data, start=1):
        team['position'] = index

    return standings_data