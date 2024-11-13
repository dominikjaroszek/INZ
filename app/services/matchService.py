# services.py
from datetime import datetime
from app.models.match import Match
from app.models.season import Season
from app.models.league import League
from app.config import db
from sqlalchemy.orm import joinedload


def get_upcoming_rounds():
    now = datetime.now()

    leagues = db.session.query(League).all()
    matches_by_league = []

    for league in leagues:
        next_match = db.session.query(Match).join(Season).join(League).filter(
            Match.type == 'Scheduled',
            League.league_name == league.league_name
        ).order_by(Match.match_date).first()

        if not next_match:
            continue

        next_round = next_match.round

        upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
            Match.round == next_round,
            League.league_name == league.league_name,
            Match.type == 'Scheduled'
        ).order_by(Match.match_date).all()

        matches_by_league.append({
            'league_name': league.league_name,
            'matches': [{
                'match_id': match.match_id,
                'home_team': match.home_team.team_name,
                'away_team': match.away_team.team_name,
                'home_team_logo': match.home_team.logo,
                'away_team_logo': match.away_team.logo,
                'match_date': match.match_date,
                'fans_rank_generally': match.fans_rank_generally,
                'fans_rank_attak': match.fans_rank_attak,
                'fans_rank_defence': match.fans_rank_defence,
                'type': match.type,
                'status': match.status_long
            } for match in upcoming_matches]
        })

    return matches_by_league




def get_upcoming_matches_by_league(league_name, limit):
    now = datetime.now()
    upcoming_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date >= now.date(),
        Match.type == 'Scheduled',
        League.league_name == league_name
    ).order_by(Match.match_date).limit(limit).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'home_team_logo': match.home_team.logo,
        'away_team_logo': match.away_team.logo,
        'away_score': match.away_score,
        'home_score': match.home_score,
        'match_date': match.match_date,
        'type': match.type,
        'status': match.status_long

    } for match in upcoming_matches]

    return matches_list

def get_finished_rounds_by_league():
    now = datetime.now()
    start_of_year = datetime(now.year, 1, 1)
    
    leagues = db.session.query(League).all()
    matches_by_league = []

    for league in leagues:
        last_match = db.session.query(Match).join(Season).join(League).filter(
            Match.match_date < now,
            Match.match_date >= start_of_year,
            Match.type == 'Not Played' or  Match.type == 'Abandoned' or Match.type == 'Finished',
            League.league_name == league.league_name
        ).order_by(Match.match_date.desc()).first()

        if not last_match:
            continue

        last_round = last_match.round

        finished_matches = db.session.query(Match).join(Season).join(League).filter(
            Match.round == last_round,
            Match.match_date >= start_of_year,
            Match.type == 'Not Played' or  Match.type == 'Abandoned' or Match.type == 'Finished',
            League.league_name == league.league_name
        ).order_by(Match.match_date.desc()).all()

        matches_by_league.append({
            'league_name': league.league_name,
            'matches': [{
                'match_id': match.match_id,
                'home_team': match.home_team.team_name,
                'away_team': match.away_team.team_name,
                'home_team_logo': match.home_team.logo,
                'away_team_logo': match.away_team.logo,
                'away_score': match.away_score,
                'home_score': match.home_score,
                'match_date': match.match_date,
                'venue_name': match.venue_name,
                'type': match.type,
                'status': match.status_long
            } for match in finished_matches]
        })


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
        Match.type == 'Not Played' or  Match.type == 'Abandoned' or Match.type == 'Finished',
    ).options(joinedload(Match.home_team), joinedload(Match.away_team)) \
     .order_by(Match.match_date.desc()).limit(limit).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'home_score': match.home_score,
        'home_team_logo': match.home_team.logo,
        'away_team_logo': match.away_team.logo,
        'away_score': match.away_score,
        'home_score': match.home_score,
        'match_date': match.match_date,
        'type': match.type,
        'status': match.status_long
    } for match in finished_matches]

    return matches_list

def get_live_matches_by_league(league_name):
    now = datetime.now()

    live_matches = db.session.query(Match).join(Season).join(League).filter(
        Match.match_date <= now,
        Match.type == 'In Play', 
        League.league_name == league_name
    ).order_by(Match.match_date).all()

    matches_list = [{
        'match_id': match.match_id,
        'home_team': match.home_team.team_name,
        'away_team': match.away_team.team_name,
        'league_name': match.season.league.league_name,
        'home_score': match.home_score,
        'away_score': match.away_score,
        'match_date': match.match_date,
        'type': match.type,
        'venue_name': match.venue_name,
        'status': match.status_long
    } for match in live_matches]

    return matches_list

def get_match_by_id(match_id):
    match = db.session.query(Match).filter(Match.match_id == match_id).first()
    if not match:
        return None
    if match.type == 'Finished':
        match_dict = {
                'match_id': match.match_id,
                'match_date': match.match_date,
                'league_name': match.season.league.league_name,
                'home_team': match.home_team.team_name,
                'away_team': match.away_team.team_name,
                'home_team_logo': match.home_team.logo,
                'away_team_logo': match.away_team.logo,
                'home_score': match.home_score,
                'away_score': match.away_score,
                'referee': match.referee,
                'match_date': match.match_date,
                'venue_name': match.venue_name,
                'round': match.round,
                'status': match.status_long,
                'home_team_shots_on_goal': match.home_team_shots_on_goal,
                'home_team_shots_off_goal': match.home_team_shots_off_goal,
                'home_team_total_shots': match.home_team_total_shots,
                'home_team_blocked_shots': match.home_team_blocked_shots,
                'home_team_shots_insidebox': match.home_team_shots_insidebox,
                'home_team_shots_outsidebox': match.home_team_shots_outsidebox,
                'home_team_fouls': match.home_team_fouls,
                'home_team_corner_kicks': match.home_team_corner_kicks,
                'home_team_offsides': match.home_team_offsides,
                'home_team_ball_possession': match.home_team_ball_possession,
                'home_team_yellow_cards': match.home_team_yellow_cards,
                'home_team_red_cards': match.home_team_red_cards,
                'home_team_goalkeeper_saves': match.home_team_goalkeeper_saves,
                'home_team_total_passes': match.home_team_total_passes,
                'home_team_passes_accuracy': match.home_team_passes_accuracy,
                'home_team_passes_percent': match.home_team_passes_percent,
                'away_team_shots_on_goal': match.away_team_shots_on_goal,
                'away_team_shots_off_goal': match.away_team_shots_off_goal,
                'away_team_total_shots': match.away_team_total_shots,
                'away_team_blocked_shots': match.away_team_blocked_shots,
                'away_team_shots_insidebox': match.away_team_shots_insidebox,
                'away_team_shots_outsidebox': match.away_team_shots_outsidebox,
                'away_team_fouls': match.away_team_fouls,
                'away_team_corner_kicks': match.away_team_corner_kicks,
                'away_team_offsides': match.away_team_offsides,
                'away_team_ball_possession': match.away_team_ball_possession,
                'away_team_yellow_cards': match.away_team_yellow_cards,
                'away_team_red_cards': match.away_team_red_cards,
                'away_team_goalkeeper_saves': match.away_team_goalkeeper_saves,
                'away_team_total_passes': match.away_team_total_passes,
                'away_team_passes_accuracy': match.away_team_passes_accuracy,
                'away_team_passes_percent': match.away_team_passes_percent,
                'season': f"{match.season.start_year}-{match.season.end_year}",
                'type': match.type

            }
    else:
        match_dict = {
                'match_id': match.match_id,
                'match_date': match.match_date,
                'league_name': match.season.league.league_name,
                'home_team': match.home_team.team_name,
                'away_team': match.away_team.team_name,
                'home_team_logo': match.home_team.logo,
                'away_team_logo': match.away_team.logo,
                'home_score': match.home_score,
                'away_score': match.away_score,
                'referee': match.referee,
                'match_date': match.match_date,
                'type': match.type,
                'venue_name': match.venue_name,
                'round': match.round,
                'status': match.status_long,
                'season': f"{match.season.start_year}-{match.season.end_year}",
                'type': match.type
            }
        
    return match_dict

def get_live_all_matches():
    matches = db.session.query(Match).filter(
        Match.type == 'In Play',
    ).all()
    matches_data = []

    for match in matches:
        matches_data.append({
            "match_id": match.match_id,
            "home_team": match.home_team.team_name,
            "away_team": match.away_team.team_name,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
        })

    return matches_data
