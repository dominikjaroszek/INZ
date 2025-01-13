from datetime import datetime
import random
from app.config import BASE_URL, db, HEADERS
import requests
from app.models.league import League
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing
from app.models.match import Match
from app.models.top_scorer import TopScorer
import time
import pytz
import re

def fetch_league_data(league_id, season):
    url = f"{BASE_URL}leagues?id={league_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data['response'][0] if response.status_code == 200 else None


def fetch_teams_data(league_id, season):
    url = f"{BASE_URL}teams"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None

def fetch_standings_data(league_id, season):
    url = f"{BASE_URL}standings"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'][0]['league']['standings'][0] if response.status_code == 200 else None


def fetch_matches_data(league_id, season):
    url = f"{BASE_URL}fixtures"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None


def fetch_top_scorers_data(league_id, season):
    url = f"{BASE_URL}players/topscorers"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None

def update_league_data(league_id, season, start_year, end_year):
    league_data = fetch_league_data(league_id, season)
    time.sleep(7)
    # Sprawdź, czy dane zostały zwrócone prawidłowo i czy istnieje odpowiedź
    if league_data and 'league' in league_data and 'seasons' in league_data:
        league_info = league_data['league']
        season_info = next((s for s in league_data['seasons'] if s['year'] == season), None)


        # Sprawdź, czy dane ligi są dostępne oraz czy jest odpowiedni sezon
        if league_info and season_info:
            # Sprawdź, czy liga istnieje już w bazie
            league = League.query.filter_by(league_id=league_info['id']).first()

            if not league:
                league = League(
                    league_id=league_info['id'], 
                    league_name=league_info['name'], 
                    country=league_data['country']['name'], 
                    logo=league_info['logo']
                )
                db.session.add(league)
                db.session.commit()

            # Sprawdź, czy sezon istnieje
            season_entry = Season.query.filter_by(league_id=league.league_id, start_year=season, end_year=season+1).first()

            if not season_entry:
                is_current = True if start_year == season and end_year == season+1 else False
                season_entry = Season(league_id=league.league_id, start_year=season, end_year=season+1, is_current=is_current)
                db.session.add(season_entry)
                db.session.commit()

            # Pobierz i zapisz drużyny
            teams_data = fetch_teams_data(league_id, season)
            time.sleep(7)
            if teams_data:
                for team_data in teams_data:
                    team = Team(team_id=team_data['team']['id'], team_name=team_data['team']['name'], league_id=league.league_id, logo=team_data['team']['logo'], venue_name=team_data['venue']['name'], city=team_data['venue']['city'], capacity=team_data['venue']['capacity'], founded=team_data['team']['founded'])
                    db.session.merge(team)
                db.session.commit()

            standings_data = fetch_standings_data(league_id, season)
            time.sleep(7)
            if standings_data:
                for standing_data in standings_data:
                    team_id = standing_data['team']['id']
                    standing_update_utc_str = standing_data['update']
                    standing_update_utc = datetime.fromisoformat(standing_update_utc_str)
                    standing_update = standing_update_utc.astimezone(pytz.timezone('Europe/Warsaw'))

                    standing = Standing(
                        season_id=season_entry.season_id,
                        team_id=team_id,
                        position=standing_data['rank'],
                        points=standing_data['points'],
                        played=standing_data['all']['played'],
                        win=standing_data['all']['win'],
                        draw=standing_data['all']['draw'],
                        lose=standing_data['all']['lose'],
                        goalsFor=standing_data['all']['goals']['for'],
                        goalsAgainst=standing_data['all']['goals']['against'],
                        goalsDifference=standing_data['goalsDiff'],
                        status=standing_data['status'],
                        lastUpdate=standing_update,
                        home_played=standing_data['home']['played'],
                        home_win=standing_data['home']['win'],
                        home_draw=standing_data['home']['draw'],
                        home_lose=standing_data['home']['lose'],
                        home_goalsFor=standing_data['home']['goals']['for'],
                        home_goalsAgainst=standing_data['home']['goals']['against'],
                        away_played=standing_data['away']['played'],
                        away_win=standing_data['away']['win'],
                        away_draw=standing_data['away']['draw'],
                        away_lose=standing_data['away']['lose'],
                        away_goalsFor=standing_data['away']['goals']['for'],
                        away_goalsAgainst=standing_data['away']['goals']['against'],
                    )
                    db.session.merge(standing)
                db.session.commit()

            matches_data = fetch_matches_data(league_id, season)
            time.sleep(7)
            if matches_data:
                for match_data in matches_data:
                    match_date_utc_str = match_data['fixture']['date']
                    match_date_utc = datetime.fromisoformat(match_date_utc_str)
                    match_date = match_date_utc.astimezone(pytz.timezone('Europe/Warsaw'))
                    
                    match = Match(
                        match_id=match_data['fixture']['id'],
                        season_id=season_entry.season_id,
                        home_team_id=match_data['teams']['home']['id'],
                        away_team_id=match_data['teams']['away']['id'],
                        home_score=match_data['goals']['home'],
                        away_score=match_data['goals']['away'],
                        referee=match_data['fixture']['referee'],
                        match_date=match_date,
                        venue_name=match_data['fixture']['venue']['name'],
                        round=match_data['league']['round'],
                        status_short=match_data['fixture']['status']['short'],
                        status_long=match_data['fixture']['status']['long'],
                        type=match_type(match_data['fixture']['status']['short']),
                    )
                    db.session.merge(match)
                db.session.commit()

            top_scorers_data = fetch_top_scorers_data(league_id, season)
            time.sleep(7)
            if top_scorers_data:
                for scorer_data in top_scorers_data:
                    top_scorer = TopScorer(
                        season_id=season_entry.season_id,
                        player_name=scorer_data['player']['name'],
                        team_id=scorer_data['statistics'][0]['team']['id'],
                        goals=scorer_data['statistics'][0]['goals']['total'],
                        assists=scorer_data['statistics'][0]['goals']['assists']
                    )
                    db.session.merge(top_scorer)
                db.session.commit()

        else:
            print(f"Brak danych dla ligi {league_id} lub brak sezonu {season}.")
    else:
        print(f"Brak danych z API dla ligi {league_id}, sezon {season}")


def match_type(short):
    if short == 'TBD':
        return 'Scheduled'
    elif short == 'NS':
        return 'Scheduled'
    elif short == '1H':
        return 'In Play'
    elif short == 'HT':
        return 'In Play'
    elif short == 'HT':
        return 'In Play'
    elif short == '2H':
        return 'In Play'
    elif short == 'ET':
        return 'In Play'
    elif short == 'BT':
        return 'In Play'
    elif short == 'P':
        return 'In Play'
    elif short == 'PEN':
        return 'In Play'
    elif short == 'SUSP':
        return 'In Play'
    elif short == 'INT':
        return 'In Play'
    elif short == 'INT':
        return 'In Play'
    elif short == 'FT':
        return 'Finished'
    elif short == 'AET':
        return 'Finished'
    elif short == 'PEN':
        return 'Finished'
    elif short == 'PST':
        return 'Postponed'
    elif short == 'CANC':
        return 'Cancelled'
    elif short == 'ABD':
        return 'Abandoned'
    elif short == 'AWD':
        return 'Not Played'
    elif short == 'WO':
        return 'Not Played'
    elif short == 'LIVE':
        return 'In Play'
    return short

# Funkcja do automatycznej aktualizacji danych dla lig 39 i 140
def update_all_data():
    for league_id in [39,140]:# for league_id in [39, 140, 78]:  for season in [2023, 2024]:
        for season in [2023, 2024]:
            update_league_data(league_id, season, 2024, 2025)   