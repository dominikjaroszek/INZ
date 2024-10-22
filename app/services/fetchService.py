from datetime import datetime
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

def fetch_team_statistics(league_id, season, team_id):
    url = f"{BASE_URL}teams/statistics"
    params = {
        "league": league_id,
        "season": season,
        "team": team_id
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    
    if response.status_code == 200 and 'response' in data:
        return data['response']
    else:
        print(f"Błąd podczas pobierania statystyk dla team_id: {team_id}, league_id: {league_id}, season: {season}")
        return None

def calculate_cards_total(team_statistics, card_color):

    cards_total = 0
    card_data = team_statistics.get('cards', {}).get(card_color, {})
    
    for time_interval, data in card_data.items():
        if 'total' in data and data['total']:
            cards_total += data['total']
    
    return cards_total


def fetch_league_data(league_id, season):
    url = f"{BASE_URL}leagues?id={league_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    return data['response'][0] if response.status_code == 200 else None

# Funkcja do pobierania drużyn
def fetch_teams_data(league_id, season):
    url = f"{BASE_URL}teams"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None

# Funkcja do pobierania tabeli (standings)
def fetch_standings_data(league_id, season):
    url = f"{BASE_URL}standings"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'][0]['league']['standings'][0] if response.status_code == 200 else None

# Funkcja do pobierania meczów
def fetch_matches_data(league_id, season):
    url = f"{BASE_URL}fixtures"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None

# Funkcja do pobierania najlepszych strzelców
def fetch_top_scorers_data(league_id, season):
    url = f"{BASE_URL}players/topscorers"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    data = response.json()
    return data['response'] if response.status_code == 200 else None

# Funkcja do automatycznego pobierania i zapisywania danych do bazy
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
                    
                    # Pobierz statystyki drużyny
                    team_statistics = fetch_team_statistics(league_id, season, team_id)
                    time.sleep(7)
                    print(team_statistics)
                    # Zsumuj żółte i czerwone kartki z danych statystycznych drużyny
                    yellow_cards_total = calculate_cards_total(team_statistics, 'yellow') if team_statistics else 0
                    red_cards_total = calculate_cards_total(team_statistics, 'red') if team_statistics else 0

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
                        form = team_statistics['form'],
                        status=standing_data['status'],
                        lastUpdate=standing_update,
                        average_goalsFor=team_statistics['goals']['for']['average']['total'],
                        average_goalsAgainst=team_statistics['goals']['against']['average']['total'],
                        failed_to_score=team_statistics['failed_to_score']['total'],
                        clean_sheet=team_statistics['clean_sheet']['total'],

                        home_played=standing_data['home']['played'],
                        home_win=standing_data['home']['win'],
                        home_draw=standing_data['home']['draw'],
                        home_lose=standing_data['home']['lose'],
                        home_goalsFor=standing_data['home']['goals']['for'],
                        average_home_goalsFor=team_statistics['goals']['for']['average']['home'],
                        average_home_goalsAgainst=team_statistics['goals']['against']['average']['home'],
                        home_goalsAgainst=standing_data['home']['goals']['against'],
                        home_failed_to_score=team_statistics['failed_to_score']['home'],
                        home_clean_sheet=team_statistics['clean_sheet']['home'],


                        away_played=standing_data['away']['played'],
                        away_win=standing_data['away']['win'],
                        away_draw=standing_data['away']['draw'],
                        away_lose=standing_data['away']['lose'],
                        away_goalsFor=standing_data['away']['goals']['for'],
                        average_away_goalsFor=team_statistics['goals']['for']['average']['away'],
                        average_away_goalsAgainst=team_statistics['goals']['against']['average']['away'],
                        away_goalsAgainst=standing_data['away']['goals']['against'],
                        away_failed_to_score=team_statistics['failed_to_score']['away'],
                        away_clean_sheet=team_statistics['clean_sheet']['away'],

                        penalty=team_statistics['penalty']['total'],
                        penalty_scored=team_statistics['penalty']['scored']['total'],
                        penalty_missed=team_statistics['penalty']['missed']['total'],


                        yellow_cards_total=yellow_cards_total,
                        red_cards_total=red_cards_total,
                    )
                    db.session.merge(standing)
                db.session.commit()



            # Pobierz i zapisz mecze
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
                        status=match_data['fixture']['status']['short']

                    )
                    db.session.merge(match)
                db.session.commit()

            # Pobierz i zapisz top scorers
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

# Funkcja do automatycznej aktualizacji danych dla lig 39 i 140
def update_all_data():
    for league_id in [39,140]:# for league_id in [39, 140, 78]:  for season in [2023, 2024]:
        for season in [2023, 2024]:
            update_league_data(league_id, season, 2024, 2025)   