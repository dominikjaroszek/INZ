from app.models.team import Team
from app.config import db
from app.models.match import Match
from datetime import datetime
from app.models.league import League
from app.models.season import Season

def get_team_by_name(team_name):
    return db.session.query(Team).filter_by(team_name=team_name).first()

def get_team(teamName):
    team = get_team_by_name(teamName)
    if not team:
        return {'error': 'Team not found'}
    
    team_data = []

    team_data = {
            "team_name": team.team_name,
            "logo": team.logo,
            "venue_name": team.venue_name,
            "city": team.city,
            "capacity": team.capacity,
            "founded": team.founded,
            "league": team.league.league_name,
            "country": team.league.country
        }

    return  team_data

def get_team_upcoming(team, limit):
    now = datetime.now()

    return db.session.query(Match).filter(
        (Match.home_team_id == team.team_id) | (Match.away_team_id == team.team_id), 
        Match.type == 'Scheduled',
        Match.match_date >= now.date()
    ).order_by(Match.match_date).limit(limit).all()

def get_upcoming_matches(team_name, limit):
    
    team = get_team_by_name(team_name)
    if not team:
        return {'error': 'Team not found'}
    
    matches = get_team_upcoming(team, limit)

    matches_data = []

    for match in matches:
        matches_data.append({
            "match_id": match.match_id,
            "home_team": match.home_team.team_name,
            "away_team": match.away_team.team_name,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
            "home_team_logo": match.home_team.logo,
            "away_team_logo": match.away_team.logo,
        })

    return matches_data

def get_team_finished(team, limit , start_year, end_year):
    now = datetime.now()

    return  db.session.query(Match).join(Season).filter(
        (Match.home_team_id == team.team_id) | (Match.away_team_id == team.team_id), 
        Match.type == 'Not Played' or  Match.type == 'Abandoned' or Match.type == 'Finished',
        Season.start_year == start_year,   
        Season.end_year == end_year,       
        Match.match_date < now,
    ).order_by(Match.match_date.desc()).limit(limit).all()

def get_finished_matches(team_name, limit, season_name):
    try:
        start_year, end_year = map(int, season_name.split('-'))
    except ValueError:
        raise ValueError("Błędny format sezonu. Prawidłowy format to 'YYYY-YYYY'.")

    team = get_team_by_name(team_name )
    if not team:
        return {'error': 'Team not found'}
    
    matches = get_team_finished(team, limit, start_year, end_year)

    matches_data = []

    for match in matches:
        matches_data.append({
            "match_id": match.match_id,
            "home_team": match.home_team.team_name,
            "away_team": match.away_team.team_name,
            "home_team_logo": match.home_team.logo,
            "away_team_logo": match.away_team.logo,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
        })

    return matches_data

def get_team_live(team):

    return db.session.query(Match).filter(
        (Match.home_team_id == team.team_id) | (Match.away_team_id == team.team_id), 
        Match.type == 'In Play',
    ).first()
    
def get_live_match(team_name):
    team = get_team_by_name(team_name)
    if not team:
        return {'error': 'Team not found'}
    
    match = get_team_live(team)
    match_data = {}
    if match:
        match_data = {
            "match_id": match.match_id,
            "home_team": match.home_team.team_name,
            "away_team": match.away_team.team_name,
            "home_team_logo": match.home_team.logo,
            "away_team_logo": match.away_team.logo,
            "home_score": match.home_score,
            "away_score": match.away_score,
            "match_date": match.match_date,
        }

    return match_data

def search_team(value):
    teams = db.session.query(Team).filter(Team.team_name.like(f'%{value}%')).all()
    leagues = db.session.query(League).filter(League.league_name.like(f'%{value}%')).all()
    teams_data = []

    for team in teams:
        teams_data.append({
            "name": team.team_name,
            "type": 'team',
            "logo": team.logo
        })
    for league in leagues:
        teams_data.append({
            "name": league.league_name,
            "logo": league.logo,
            "type": 'league',
        })

    return teams_data