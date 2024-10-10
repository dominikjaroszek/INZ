# services.py
from datetime import datetime
from app.models.match import Match
from app.models.season import Season
from app.models.league import League
from app.config import db



def get_upcoming_round():
    now = datetime.now()

    # Pobierz datę najbliższego meczu
    next_match = db.session.query(Match).filter(
        Match.match_date >= now
    ).order_by(Match.match_date).first()

    if not next_match:
        return {}

    # Pobierz kolejkę najbliższego meczu
    next_round = next_match.round

    # Pobierz wszystkie mecze z tej kolejki
    upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.round == next_round,
        Match.match_date >= now
    ).order_by(Match.match_date).all()

    matches_by_league = {}
    for match in upcoming_matches:
        league_name = match.season.league.league_name
        
        if league_name not in matches_by_league:
            matches_by_league[league_name] = []
        
        matches_by_league[league_name].append({
            'match_id': match.match_id,
            'home_team': match.home_team.team_name,
            'away_team': match.away_team.team_name,
            'match_date': match.match_date,
            'venue_name': match.venue_name,
            'status': match.status
        })

    return matches_by_league


def get_upcoming_matches_by_league(league_name, limit):
    now = datetime.now()
    upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date >= now,
        League.league_name == league_name
    ).order_by(Match.match_date).limit(limit).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'match_date': match.match_date,
        'venue_name': match.venue_name,
        'status': match.status
    } for match in upcoming_matches]

    return matches_list

def get_finished_round():
    now = datetime.now()

    # Pobierz datę ostatniego zakończonego meczu
    last_match = db.session.query(Match).filter(
        Match.match_date < now
    ).order_by(Match.match_date.desc()).first()

    if not last_match:
        return {}

    # Pobierz kolejkę ostatniego meczu
    last_round = last_match.round

    # Pobierz wszystkie mecze z tej kolejki
    finished_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.round == last_round,
        Match.match_date < now
    ).order_by(Match.match_date.desc()).all()

    matches_by_league = {}
    for match in finished_matches:
        league_name = match.season.league.league_name
        
        if league_name not in matches_by_league:
            matches_by_league[league_name] = []
        
        matches_by_league[league_name].append({
            'match_id': match.match_id,
            'home_team': match.home_team.team_name,
            'away_team': match.away_team.team_name,
            'home_score': match.home_score,
            'away_score': match.away_score,
            'match_date': match.match_date,
            'venue_name': match.venue_name,
            'status': match.status
        })

    return matches_by_league

# Funkcja do pobrania określonej liczby zakończonych meczów z wybranej ligi
def get_finished_matches_by_league(league_name, limit):
    now = datetime.now()
    finished_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date < now,
        League.league_name == league_name
    ).order_by(Match.match_date.desc()).limit(limit).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'home_score': match.home_score,
        'away_score': match.away_score,
        'match_date': match.match_date,
        'venue_name': match.venue_name,
        'status': match.status
    } for match in finished_matches]

    return matches_list