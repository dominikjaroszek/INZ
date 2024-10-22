# services.py
from datetime import datetime
from app.models.match import Match
from app.models.season import Season
from app.models.league import League
from app.config import db
from sqlalchemy.orm import joinedload


def get_upcoming_rounds():
    now = datetime.now()

    # Pobierz najbliższą kolejkę dla każdej ligi
    leagues = db.session.query(League).all()
    matches_by_league = {}

    for league in leagues:
        # Pobierz najbliższy mecz dla danej ligi
        next_match = db.session.query(Match).join(Season).join(League).filter(
            Match.match_date >= now.date(),
            League.league_name == league.league_name
        ).order_by(Match.match_date).first()

        if not next_match:
            continue

        # Pobierz numer kolejki najbliższego meczu
        next_round = next_match.round

        # Pobierz wszystkie mecze z tej kolejki w danej lidze
        upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
            Match.round == next_round,
            League.league_name == league.league_name,
            Match.match_date >= now
        ).order_by(Match.match_date).all()

        # Dodaj mecze do słownika wg ligi
        league_name = league.league_name
        matches_by_league[league_name] = [{
            'match_id': match.match_id,
            'home_team': match.home_team.team_name,
            'away_team': match.away_team.team_name,
            'match_date': match.match_date,
            'venue_name': match.venue_name,
            'status': match.status
        } for match in upcoming_matches]

    return matches_by_league



def get_upcoming_matches_by_league(league_name, limit):
    now = datetime.now()
    upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date >= now.date(),
        Match.status == 'NS',
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

def get_finished_rounds_by_league():
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    
    leagues = db.session.query(League).all()
    matches_by_league = {}

    for league in leagues:
        # Pobierz ostatni zakończony mecz z bieżącego roku dla danej ligi
        last_match = db.session.query(Match).join(Season).join(League).filter(
            Match.match_date < now,
            Match.match_date >= start_of_year,
            Match.status == 'FT',
            League.league_name == league.league_name
        ).order_by(Match.match_date.desc()).first()

        if not last_match:
            continue

        # Pobierz numer kolejki ostatniego meczu
        last_round = last_match.round

        # Pobierz wszystkie mecze z tej kolejki o statusie FT z bieżącego roku
        finished_matches = db.session.query(Match).join(Season).join(League).filter(
            Match.round == last_round,
            Match.match_date >= start_of_year,
            Match.status == 'FT',
            League.league_name == league.league_name
        ).order_by(Match.match_date.desc()).all()

        # Dodaj mecze do słownika wg ligi
        league_name = league.league_name
        matches_by_league[league_name] = [{
            'match_id': match.match_id,
            'home_team': match.home_team.team_name,
            'away_team': match.away_team.team_name,
            'home_score': match.home_score,
            'away_score': match.away_score,
            'match_date': match.match_date,
            'venue_name': match.venue_name,
            'status': match.status
        } for match in finished_matches]

    return matches_by_league



# Funkcja do pobrania określonej liczby zakończonych meczów z wybranej ligi
def get_finished_matches_by_league(league_name, limit, season_name):
    now = datetime.now()

    # Wyodrębnij lata z season_name
    try:
        start_year, end_year = map(int, season_name.split('-'))
    except ValueError:
        raise ValueError("Błędny format sezonu. Prawidłowy format to 'YYYY-YYYY'.")

    finished_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date < now,
        League.league_name == league_name,
        Season.start_year == start_year,   # Filtrowanie po roku rozpoczęcia sezonu
        Season.end_year == end_year,       # Filtrowanie po roku zakończenia sezonu
        Match.status == 'FT'
    ).options(joinedload(Match.home_team), joinedload(Match.away_team)) \
     .order_by(Match.match_date.desc()).limit(limit).all()

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

def get_live_matches_by_league(league_name):
    now = datetime.now()

    live_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date <= now,
        Match.status == 'LIVE',
        League.league_name == league_name
    ).order_by(Match.match_date).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'home_score': match.home_score,
        'away_score': match.away_score,
        'match_date': match.match_date,
        'venue_name': match.venue_name,
        'status': match.status
    } for match in live_matches]

    return matches_list