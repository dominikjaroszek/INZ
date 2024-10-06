from app.config import API_KEY, BASE_URL,db
import requests
from app.models.league import League
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing
from app.models.match import Match
from app.models.top_scorer import TopScorer
from app.config import API_KEY, BASE_URL, HEADERS
import time

# def get_league_coverage():
#     for id_league in ids:
#         # Pobieranie dostępnych sezonów od roku 2023
#         for season in range(since, 2025):  # Załóżmy, że pobieramy dane do sezonu 2023/24
#             url = f'{BASE_URL}/leagues?id={id_league}&season={season}'
#             headers = {
#                 'x-rapidapi-key': API_KEY,
#                 'x-rapidapi-host': 'v3.football.api-sports.io'
#             }
#             response = requests.get(url, headers=headers)
#             if response.status_code == 200:
#                 data = response.json()
#                 leagues = data.get('response', [])
                
#                 # Iteracja po ligach i zapis do bazy danych
#                 for league_data in leagues:
#                     league_info = league_data['league']
#                     country_info = league_data['country']

#                     # Sprawdzanie, czy liga z danym IdS (ID ligi z API) i sezonem już istnieje w bazie danych
#                     existing_league = League.query.filter_by(IdS=league_info['id'], Season=str(season)).first()

#                     if not existing_league:
#                         # Tworzenie nowej ligi
#                         new_league = League(
#                             IdS=league_info['id'],  # IdS to ID ligi z API
#                             NameLeague=league_info['name'],
#                             Country=country_info['name'],
#                             Logo=league_info['logo'],
#                             Season=str(season)
#                         )
#                         db.session.add(new_league)

#                 db.session.commit()
#     return None

def fetch_league_data(league_id, season):
    url = f"{BASE_URL}leagues?id={league_id}&season={season}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()
    print(data)
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
def update_league_data(league_id, season):
    league_data = fetch_league_data(league_id, season)
    
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
                    name_league=league_info['name'], 
                    country=league_data['country']['name'], 
                    logo=league_info['logo']
                )
                db.session.add(league)
                db.session.commit()

            # Sprawdź, czy sezon istnieje
            season_entry = Season.query.filter_by(league_id=league.league_id, start_year=season, end_year=season).first()

            if not season_entry:
                season_entry = Season(league_id=league.league_id, start_year=season, end_year=season+1)
                db.session.add(season_entry)
                db.session.commit()

            # Pobierz i zapisz drużyny
            teams_data = fetch_teams_data(league_id, season)
            if teams_data:
                for team_data in teams_data:
                    team = Team(team_id=team_data['team']['id'], nameTeam=team_data['team']['name'], league_id=league.league_id, logo=team_data['team']['logo'], nameVenue=team_data['venue']['name'], city=team_data['venue']['city'], capacity=team_data['venue']['capacity'], founded=team_data['team']['founded'])
                    db.session.merge(team)
                db.session.commit()

            # Pobierz i zapisz standings
            standings_data = fetch_standings_data(league_id, season)
            if standings_data:
                for standing_data in standings_data:
                    team_id = standing_data['team']['id']
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
                        form=standing_data['form'],
                        status=standing_data['status'],
                        lastUpdate=standing_data['update'],

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

            # Pobierz i zapisz mecze
            matches_data = fetch_matches_data(league_id, season)
            if matches_data:
                for match_data in matches_data:
                    match = Match(
                        match_id=match_data['fixture']['id'],
                        season_id=season_entry.season_id,
                        home_team_id=match_data['teams']['home']['id'],
                        away_team_id=match_data['teams']['away']['id'],
                        home_score=match_data['goals']['home'],
                        away_score=match_data['goals']['away'],

                        timezone=match_data['fixture']['timezone'],
                        match_date=match_data['fixture']['date'],
                        venueName=match_data['fixture']['venue']['name'],
                        round=match_data['league']['round'],
                        status=match_data['fixture']['status']['short']

                    )
                    db.session.merge(match)
                db.session.commit()

            # Pobierz i zapisz top scorers
            top_scorers_data = fetch_top_scorers_data(league_id, season)
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
    for league_id in [39, 140, 78]:
        for season in [2023, 2024]:
            update_league_data(league_id, season)   
            time.sleep(61)  