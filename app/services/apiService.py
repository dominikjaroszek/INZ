from datetime import datetime
import random
from app.config import BASE_URL, db, HEADERS
import requests
from app.models.season import Season
from app.models.team import Team
from app.models.standing import Standing
from app.models.match import Match
from app.models.top_scorer import TopScorer
from app.services.fetchService import *
import pytz
import time
from app.services.standingService import get_standing_team, get_season_by_league_id_and_current_season, get_standing_by_team_and_season_id
from app.services.matchService import finished_last_match,next_round_league, get_upcoming_matches_by_round, get_match_by_type_and_season


def oblicz_faule(match):
    return (match.home_team_fouls or 0) + (match.away_team_fouls or 0)

def oblicz_zolte_kartki(match):
    return (match.home_team_yellow_cards or 0) + (match.away_team_yellow_cards or 0)

def oblicz_czerwone_kartki(match):
    return (match.home_team_red_cards or 0) + (match.away_team_red_cards or 0)

def oblicz_statystyki_druzyny(recent_matches):
    fouls, yellow_cards, red_cards = 0, 0, 0

    for match in recent_matches:
        fouls += oblicz_faule(match)
        yellow_cards += oblicz_zolte_kartki(match)
        red_cards += oblicz_czerwone_kartki(match)

    max_fouls = 25 * len(recent_matches)
    max_yellow_cards = 5 * len(recent_matches)
    max_red_cards = 2 * len(recent_matches)

    fouls = min(fouls, max_fouls)
    yellow_cards = min(yellow_cards, max_yellow_cards)
    red_cards = min(red_cards, max_red_cards)

    return znormalizuj_wg(fouls, yellow_cards, red_cards, max_fouls, max_yellow_cards, max_red_cards)


def znormalizuj_wg(fouls, yellow_cards, red_cards, max_fouls, max_yellow_cards, max_red_cards):
    wg_raw = 0.4 * fouls + 0.35 * yellow_cards + 0.25 * red_cards
    max_wg = 0.4 * max_fouls + 0.35 * max_yellow_cards + 0.25 * max_red_cards
    return (wg_raw / max_wg * 100) if max_wg > 0 else 0


def oblicz_wskaznik_agresji(match):
    team1_id = match.home_team_id
    team2_id = match.away_team_id

    matches_team1 = finished_last_match(team1_id, match.season.start_year, match.season.end_year, 5)
    matches_team2 = finished_last_match(team2_id, match.season.start_year, match.season.end_year, 5)

    wg_team1 = oblicz_statystyki_druzyny(matches_team1)
    wg_team2 = oblicz_statystyki_druzyny(matches_team2)

    return wylicz_wazona_srednia(wg_team1, wg_team2, waga_team1=0.6, waga_team2=0.4)


def wylicz_wazona_srednia(wg_team1, wg_team2, waga_team1=0.6, waga_team2=0.4):
    return round((wg_team1 * waga_team1 + wg_team2 * waga_team2) / (waga_team1 + waga_team2), 2)


def oblicz_possession(match):
    return (match.home_team_ball_possession or 0) + (match.away_team_ball_possession or 0)

def oblicz_corners(match):
    return (match.home_team_corner_kicks or 0) + (match.away_team_corner_kicks or 0)

def oblicz_goals(match):
    return (match.home_score or 0) + (match.away_score or 0)

def oblicz_shots(match):
    return (match.home_team_total_shots or 0) + (match.away_team_total_shots or 0)

def oblicz_penalties(match):
    return (match.home_team_offsides or 0) + (match.away_team_offsides or 0)

def oblicz_wskaznik_wg_bramkoszczelnosc(match):
    team1_id = match.home_team_id
    team2_id = match.away_team_id

    matches_team1 = finished_last_match(team1_id, match.season.start_year, match.season.end_year, 5)
    matches_team2 = finished_last_match(team2_id, match.season.start_year, match.season.end_year, 5)

    wg_team1 = oblicz_statystyki_bramkoszczelnosci(matches_team1)
    wg_team2 = oblicz_statystyki_bramkoszczelnosci(matches_team2)

    return wylicz_srednia_wazona(wg_team1, wg_team2, waga_team1=0.6, waga_team2=0.4)


def oblicz_statystyki_bramkoszczelnosci(recent_matches):
    possession, corners, goals, shots, penalties = 0, 0, 0, 0, 0

    for match in recent_matches:
        possession += oblicz_possession(match)
        corners += oblicz_corners(match)
        goals += oblicz_goals(match)
        shots += oblicz_shots(match)
        penalties += oblicz_penalties(match)

    max_values = {
        "possession": 70 * len(recent_matches),
        "corners": 10 * len(recent_matches),
        "goals": 5 * len(recent_matches),
        "shots": 20 * len(recent_matches),
        "penalties": 10 * len(recent_matches),
    }

    values = {
        "possession": min(possession, max_values["possession"]),
        "corners": min(corners, max_values["corners"]),
        "goals": min(goals, max_values["goals"]),
        "shots": min(shots, max_values["shots"]),
        "penalties": min(penalties, max_values["penalties"]),
    }

    return znormalizuj_wg_bramkoszczelnosci(values, max_values)


def znormalizuj_wg_bramkoszczelnosci(values, max_values):
    wg_raw = (
        0.3 * values["possession"] +
        0.1 * values["corners"] +
        0.5 * values["goals"] +
        0.3 * values["shots"] +
        0.4 * values["penalties"]
    )
    max_wg = (
        0.3 * max_values["possession"] +
        0.1 * max_values["corners"] +
        0.5 * max_values["goals"] +
        0.3 * max_values["shots"] +
        0.4 * max_values["penalties"]
    )
    return (wg_raw / max_wg * 100) if max_wg > 0 else 0


def wylicz_srednia_wazona(wg_team1, wg_team2, waga_team1=0.6, waga_team2=0.4):
   
    return round((wg_team1 * waga_team1 + wg_team2 * waga_team2) / (waga_team1 + waga_team2), 2)



def oblicz_form(standing):
    form = 0
    for value in (standing.form or ""):
        if value == "W":
            form += 3
        elif value == "D":
            form += 1
    return form

def oblicz_ofensywa(recent_matches):
    offense = 0
    for match in recent_matches:
        offense += (match.home_score or 0) + (match.away_score or 0)
    return offense

def oblicz_obrona(recent_matches):
    defense = 0
    for match in recent_matches:
        defense += (match.away_score or 0) + (match.home_score or 0)
    return defense

def oblicz_wskaznik_wg_ogolna(match):
    team1_id = match.home_team_id
    team2_id = match.away_team_id

    matches_team1 = finished_last_match(team1_id, match.season.start_year, match.season.end_year, 5)
    matches_team2 = finished_last_match(team2_id, match.season.start_year, match.season.end_year, 5)

    standing1 = get_standing_team(team1_id, match.season.season_id)
    standing2 = get_standing_team(team2_id, match.season.season_id)

    weight = oblicz_wage(standing1.position, standing2.position)

    wg_team1 = oblicz_statystyki_wg(matches_team1, standing1)
    wg_team2 = oblicz_statystyki_wg(matches_team2, standing2)

    return wylicz_srednia_wazona_weight(wg_team1, wg_team2, weight)


def oblicz_wage(rank1, rank2):
    if rank1 <= 3 and rank2 <= 3:
        return 1.0
    elif (rank1 <= 3 and 4 <= rank2 <= 8) or (rank2 <= 3 and 4 <= rank1 <= 8):
        return 0.85
    elif (rank1 <= 3 and 9 <= rank2 <= 15) or (rank2 <= 3 and 9 <= rank1 <= 15):
        return 0.7
    elif (rank1 <= 3 and rank2 > 15) or (rank2 <= 3 and rank1 > 15):
        return 0.5
    elif (4 <= rank1 <= 8 and 4 <= rank2 <= 8):
        return 0.75
    elif (4 <= rank1 <= 8 and rank2 > 15) or (4 <= rank2 <= 8 and rank1 > 15):
        return 0.6
    elif rank1 > 15 and rank2 > 15:
        return 0.4
    else:
        return 0.5


def oblicz_statystyki_wg(recent_matches, standing):
    form = oblicz_form(standing)
    offense = oblicz_ofensywa(recent_matches)
    defense = oblicz_obrona(recent_matches)

    max_form = 15
    max_offense = 30
    max_defense = 30

    form = min(max_form, form)
    offense = min(max_offense, offense)
    defense = max(0, max_defense - defense)

    return znormalizuj_wg(form, offense, defense, max_form, max_offense, max_defense)


def znormalizuj_wg(form, offense, defense, max_form, max_offense, max_defense):
    wg_raw = 0.4 * form + 0.3 * offense + 0.1 * defense
    max_wg = 0.4 * max_form + 0.3 * max_offense + 0.1 * max_defense
    return (wg_raw / max_wg * 100) if max_wg > 0 else 0


def wylicz_srednia_wazona_weight(wg_team1, wg_team2, weight):
    waga_team1 = 0.6 * weight
    waga_team2 = 0.4 * weight
    return round((wg_team1 * waga_team1 + wg_team2 * waga_team2) / (waga_team1 + waga_team2), 2)

def update_wskazniki(league_id):

    next_round = next_round_league(league_id)

    upcoming_matches = get_upcoming_matches_by_round(league_id, next_round)

    for match in upcoming_matches:
        wg_agresji = oblicz_wskaznik_agresji(match)
        wg_bramkoszczelnosc = oblicz_wskaznik_wg_bramkoszczelnosc(match)
        wg_ogolna = oblicz_wskaznik_wg_ogolna(match)

        match.fans_rank_defence = wg_agresji
        match.fans_rank_attak = wg_bramkoszczelnosc
        match.fans_rank_generally = wg_ogolna

        db.session.merge(match)
        db.session.commit()


def fetch_match_statistics(match_id):
    url = f"{BASE_URL}fixtures/statistics"
    params = {"fixture": match_id}

    try:
        response = requests.get(url, headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Błąd połączenia z API: {e}")
        return None
    except ValueError:
        print("Niepoprawna odpowiedź JSON")
        return None

def check_results(league_id):
    season = Season.query.filter_by(league_id=league_id, is_current=True).first()
    matches = Match.query.filter(Match.type == "Scheduled", Match.season == season).all()
    matches = sorted(matches, key=lambda x: x.match_date)
    matches = matches[:5]

    for match in matches:
        url = f"{BASE_URL}fixtures/statistics"
        params = {"fixture": match.match_id}

        try:
            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status() 
            data = response.json()
        except requests.RequestException as e:
            print(f"Błąd połączenia z API: {e}")
            continue  
        except ValueError:
            print("Niepoprawna odpowiedź JSON")
            continue

       
        if data.get("results", 0) > 0 and "response" in data:
            print(f"Znaleziono dane dla meczu {match.match_id}")
            return True
        else:
            print(f"Brak wyników dla meczu {match.match_id}: {data}")

    print("Zakończono sprawdzanie wyników brak nowych wyników")
    return False

def calculate_cards_total(team_statistics, card_color):

    cards_total = 0
    card_data = team_statistics.get('cards', {}).get(card_color, {})
    
    for time_interval, data in card_data.items():
        if 'total' in data and data['total']:
            cards_total += data['total']
    
    return cards_total


def update_standing(league_id):
    season = Season.query.filter_by(league_id=league_id, is_current=True).first()
    season_start = season.start_year if season else None
  
    standings = fetch_standings_data(league_id, season_start)
    time.sleep(7)
    for standing_data in standings:
        team_id = standing_data['team']['id']
        team = Team.query.get(team_id)
        if not team:
            continue
        standing_db = Standing.query.filter_by(team_id=team_id, season_id=season.season_id).first()

        if standing_db:
            print(f"Znaleziono rekord dla drużyny {team.team_name}")
      
        if not standing_db:
            standing_db = Standing(team_id=team_id)

        standing_update_utc_str = standing_data['update']
        standing_update_utc = datetime.fromisoformat(standing_update_utc_str)
        standing_update = standing_update_utc.astimezone(pytz.timezone('Europe/Warsaw'))

        
        standing_db.position = standing_data["rank"]
        standing_db.points = standing_data["points"]
        standing_db.played = standing_data['all']['played']
        standing_db.win = standing_data['all']['win']
        standing_db.draw = standing_data['all']['draw']
        standing_db.lose = standing_data['all']['lose']
        standing_db.goalsFor = standing_data['all']['goals']['for']
        standing_db.goalsAgainst = standing_data['all']['goals']['against']
        standing_db.goalsDifference = standing_data['goalsDiff']
        standing_db.status = standing_data['status']
        standing_db.lastUpdate = standing_update
        standing_db.home_played = standing_data['home']['played']
        standing_db.home_win = standing_data['home']['win']
        standing_db.home_draw = standing_data['home']['draw']
        standing_db.home_lose = standing_data['home']['lose']
        standing_db.home_goalsFor = standing_data['home']['goals']['for']
        standing_db.home_goalsAgainst = standing_data['home']['goals']['against']
        standing_db.away_played = standing_data['away']['played']
        standing_db.away_win = standing_data['away']['win']
        standing_db.away_draw = standing_data['away']['draw']
        standing_db.away_lose = standing_data['away']['lose']
        standing_db.away_goalsFor = standing_data['away']['goals']['for']
        standing_db.away_goalsAgainst = standing_data['away']['goals']['against']

   
        db.session.merge(standing_db)
    db.session.commit()


def update_top_scorers(league_id):
    
    season = Season.query.filter_by(league_id=league_id, is_current=True).first()
    if not season:
        raise ValueError(f"Brak aktywnego sezonu dla league_id: {league_id}")
    
    season_id = season.season_id  
    top_scorers_data = fetch_top_scorers_data(league_id, season.start_year)
    time.sleep(7)
    
    if top_scorers_data:
        for scorer_data in top_scorers_data:
            player_name = scorer_data['player']['name']
            team_id = scorer_data['statistics'][0]['team']['id']
            goals = scorer_data['statistics'][0]['goals']['total']
            assists = scorer_data['statistics'][0]['goals']['assists']

           
            top_scorer = TopScorer.query.filter_by(
                season_id=season_id,
                player_name=player_name,
                team_id=team_id
            ).first()

            if top_scorer:
              
                top_scorer.goals = goals
                top_scorer.assists = assists
                db.session.merge(top_scorer)  
            else:

                new_top_scorer = TopScorer(
                    season_id=season_id,
                    player_name=player_name,
                    team_id=team_id,
                    goals=goals,
                    assists=assists,
                )
                db.session.add(new_top_scorer)
            
        db.session.commit()  

import requests

def update_matches(league_id):
    now = datetime.now()

    season = Season.query.filter_by(league_id=league_id, is_current=True).first()
    season_year = season.start_year if season else None

   
    matches_scheduled = Match.query.filter(
        Match.type == "Scheduled", Match.season_id == season.season_id, Match.match_date < now
    ).all()

   
    matches_data = fetch_matches_data(league_id, season_year)
    time.sleep(7)
    for match in matches_scheduled:
        
        match_data = next((x for x in matches_data if x['fixture']['id'] == match.match_id), None)
        if match_data:
            
            match.home_score = match_data['goals']['home']
            match.away_score = match_data['goals']['away']
            match.referee =match_data['fixture']['referee'],
            match.venue_name = match_data['fixture']['venue']['name']
            match.round = match_data['league']['round']
            match.status_short = match_data['fixture']['status']['short']
            match.status_long = match_data['fixture']['status']['long']
            match.type=match_type(match_data['fixture']['status']['short']),

            
            stats_url = f"{BASE_URL}fixtures/statistics?fixture={match.match_id}"
            response = requests.get(stats_url, headers=HEADERS)
            if response.status_code == 200:
                stats_data = response.json().get('response', [])
                time.sleep(7)
                
                stats_dict = {}
                for team_stats in stats_data:
                    team_id = team_stats['team']['id']
                    team_statistics = {stat['type']: stat['value'] for stat in team_stats['statistics']}
                    stats_dict[team_id] = team_statistics

               
                home_stats = stats_dict.get(match.home_team_id, {})
                match.home_team_shots_on_goal = home_stats.get("Shots on Goal", None)
                match.home_team_shots_off_goal = home_stats.get("Shots off Goal", None)
                match.home_team_total_shots = home_stats.get("Total Shots", None)
                match.home_team_blocked_shots = home_stats.get("Blocked Shots", None)
                match.home_team_shots_insidebox = home_stats.get("Shots insidebox", None)
                match.home_team_shots_outsidebox = home_stats.get("Shots outsidebox", None)
                match.home_team_fouls = home_stats.get("Fouls", None)
                match.home_team_corner_kicks = home_stats.get("Corner Kicks", None)
                match.home_team_offsides = home_stats.get("Offsides", None)
                match.home_team_ball_possession = (
                    float(home_stats.get("Ball Possession", "0%").replace("%", "")) if "Ball Possession" in home_stats else None
                )
                match.home_team_yellow_cards = home_stats.get("Yellow Cards", None)
                match.home_team_red_cards = home_stats.get("Red Cards", None)
                match.home_team_goalkeeper_saves = home_stats.get("Goalkeeper Saves", None)
                match.home_team_total_passes = home_stats.get("Total passes", None)
                match.home_team_passes_accuracy = home_stats.get("Passes accurate", None)
                match.home_team_passes_percent = (
                    float(home_stats.get("Passes %", "0%").replace("%", "")) if "Passes %" in home_stats else None
                )

              
                away_stats = stats_dict.get(match.away_team_id, {})
                match.away_team_shots_on_goal = away_stats.get("Shots on Goal", None)
                match.away_team_shots_off_goal = away_stats.get("Shots off Goal", None)
                match.away_team_total_shots = away_stats.get("Total Shots", None)
                match.away_team_blocked_shots = away_stats.get("Blocked Shots", None)
                match.away_team_shots_insidebox = away_stats.get("Shots insidebox", None)
                match.away_team_shots_outsidebox = away_stats.get("Shots outsidebox", None)
                match.away_team_fouls = away_stats.get("Fouls", None)
                match.away_team_corner_kicks = away_stats.get("Corner Kicks", None)
                match.away_team_offsides = away_stats.get("Offsides", None)
                match.away_team_ball_possession = (
                    float(away_stats.get("Ball Possession", "0%").replace("%", "")) if "Ball Possession" in away_stats else None
                )
                match.away_team_yellow_cards = away_stats.get("Yellow Cards", None)
                match.away_team_red_cards = away_stats.get("Red Cards", None)
                match.away_team_goalkeeper_saves = away_stats.get("Goalkeeper Saves", None)
                match.away_team_total_passes = away_stats.get("Total passes", None)
                match.away_team_passes_accuracy = away_stats.get("Passes accurate", None)
                match.away_team_passes_percent = (
                    float(away_stats.get("Passes %", "0%").replace("%", "")) if "Passes %" in away_stats else None
                )
                print(f"Zaktualizowano mecz {match.match_id}")
                db.session.commit()


def update_standing_form():
    seasons = Season.query.all()
    for season in seasons:
        season_id = season.season_id

        teams = Team.query.join(Match, (Match.home_team_id == Team.team_id) | (Match.away_team_id == Team.team_id)) \
                        .filter(Match.season_id == season_id) \
                        .distinct()

        for team in teams:
            matches_home = Match.query.filter_by(home_team_id=team.team_id, season_id=season_id, type = "Finished").order_by(Match.match_date.desc()).all()
            matches_away = Match.query.filter_by(away_team_id=team.team_id, season_id=season_id, type = "Finished").order_by(Match.match_date.desc()).all()
            all_matches = sorted(matches_home + matches_away, key=lambda x: x.match_date, reverse=True)
            recent_matches = all_matches[:5]  

            form = ""
            for match in recent_matches:
                if match.status_short == "FT":  
                    if match.home_team_id == team.team_id:
                        if match.home_score > match.away_score:
                            form += "W"
                        elif match.home_score == match.away_score:
                            form += "D"
                        else:
                            form += "L"
                    elif match.away_team_id == team.team_id:
                        if match.away_score > match.home_score:
                            form += "W"
                        elif match.away_score == match.home_score:
                            form += "D"
                        else:
                            form += "L"
                    
            standing = Standing.query.filter_by(team_id=team.team_id, season_id=season_id).first()
            if standing:
                standing.form = form[::-1]

                db.session.merge(standing)

            db.session.commit()



def extract_round_number(round_name):
    
    match = re.search(r'\d+', round_name)
    return int(match.group()) if match else 0


def update_match_details_back(league_id):
   
    season = Season.query.filter_by(is_current=True, league_id=league_id).first()

    
    matches = Match.query.join(Season).filter(
        Match.type == 'Finished',
        Season.season_id == season.season_id
    ).all()

    
    matches = sorted(matches, key=lambda x: extract_round_number(x.round), reverse=True)

    
    rounds = set()
    limited_matches = []
    for match in matches:
        round_number = extract_round_number(match.round)
        if len(rounds) < 5:
            rounds.add(round_number)
            limited_matches.append(match)
        elif round_number in rounds:
            limited_matches.append(match)
        else:
            continue

    for match in limited_matches:
        stats_url = f"{BASE_URL}fixtures/statistics?fixture={match.match_id}"
        response = requests.get(stats_url, headers=HEADERS)
        if response.status_code == 200:
            stats_data = response.json().get('response', [])
            time.sleep(7)
           
            stats_dict = {}
            for team_stats in stats_data:
                team_id = team_stats['team']['id']
                team_statistics = {stat['type']: stat['value'] for stat in team_stats['statistics']}
                stats_dict[team_id] = team_statistics

          
            home_stats = stats_dict.get(match.home_team_id, {})
            match.home_team_shots_on_goal = home_stats.get("Shots on Goal", 0)
            match.home_team_shots_off_goal = home_stats.get("Shots off Goal", 0)
            match.home_team_total_shots = home_stats.get("Total Shots", 0)
            match.home_team_blocked_shots = home_stats.get("Blocked Shots", 0)
            match.home_team_shots_insidebox = home_stats.get("Shots insidebox", 0)
            match.home_team_shots_outsidebox = home_stats.get("Shots outsidebox", 0)
            match.home_team_fouls = home_stats.get("Fouls", 0)
            match.home_team_corner_kicks = home_stats.get("Corner Kicks", 0)
            match.home_team_offsides = home_stats.get("Offsides", 0)
            match.home_team_ball_possession = (
                float(home_stats.get("Ball Possession", "0%" ).replace("%", "")) if "Ball Possession" in home_stats else 0
            )
            match.home_team_yellow_cards = home_stats.get("Yellow Cards", 0)
            match.home_team_red_cards = home_stats.get("Red Cards", 0)
            match.home_team_goalkeeper_saves = home_stats.get("Goalkeeper Saves", 0)
            match.home_team_total_passes = home_stats.get("Total passes", 0)
            match.home_team_passes_accuracy = home_stats.get("Passes accurate", 0)
            match.home_team_passes_percent = (
                float(home_stats.get("Passes %", "0%").replace("%", "")) if "Passes %" in home_stats else 0
            )

          
            away_stats = stats_dict.get(match.away_team_id, {})
            match.away_team_shots_on_goal = away_stats.get("Shots on Goal", 0)
            match.away_team_shots_off_goal = away_stats.get("Shots off Goal", 0)
            match.away_team_total_shots = away_stats.get("Total Shots", 0)
            match.away_team_blocked_shots = away_stats.get("Blocked Shots", 0)
            match.away_team_shots_insidebox = away_stats.get("Shots insidebox", 0)
            match.away_team_shots_outsidebox = away_stats.get("Shots outsidebox", 0)
            match.away_team_fouls = away_stats.get("Fouls", 0)
            match.away_team_corner_kicks = away_stats.get("Corner Kicks", 0)
            match.away_team_offsides = away_stats.get("Offsides", 0)
            match.away_team_ball_possession = (
                float(away_stats.get("Ball Possession", "0%").replace("%", "")) if "Ball Possession" in away_stats else 0
            )
            match.away_team_yellow_cards = away_stats.get("Yellow Cards", 0)
            match.away_team_red_cards = away_stats.get("Red Cards", 0)
            match.away_team_goalkeeper_saves = away_stats.get("Goalkeeper Saves", 0)
            match.away_team_total_passes = away_stats.get("Total passes", 0)
            match.away_team_passes_accuracy = away_stats.get("Passes accurate", 0)
            match.away_team_passes_percent = (
                float(away_stats.get("Passes %", "0%").replace("%", "")) if "Passes %" in away_stats else 0
            )
            print(f"Zaktualizowano mecz {match.match_id}")
            db.session.commit()



def update_league(league_id):
    update_standing(league_id)
    update_matches(league_id)
    update_standing_form()
    update_top_scorers(league_id)
    update_wskazniki(league_id)
    print("Zaktualizowano dane ligi")

def check_update(league_id):
    if check_results(league_id):
        update_league(league_id)
    else:
        print("Brak nowych wyników")


import random

def update_match_details_back_test(league_id):
   
    season = Season.query.filter_by(is_current=True, league_id=league_id).first()

    matches = Match.query.join(Season).filter(
        Match.type == 'Finished',
        Season.season_id == season.season_id
    ).all()

    matches = sorted(matches, key=lambda x: extract_round_number(x.round), reverse=True)

    rounds = set()
    limited_matches = []
    for match in matches:
        round_number = extract_round_number(match.round)
        if len(rounds) < 5:
            rounds.add(round_number)
            limited_matches.append(match)
        elif round_number in rounds:
            limited_matches.append(match)
        else:
            continue

    for match in limited_matches:
        
        match.home_team_shots_on_goal = random.randint(1, 10)
        match.home_team_shots_off_goal = random.randint(1, 10)
        match.home_team_total_shots = random.randint(1, 10)
        match.home_team_blocked_shots = random.randint(1, 10)
        match.home_team_shots_insidebox = random.randint(1, 10)
        match.home_team_shots_outsidebox = random.randint(1, 10)
        match.home_team_fouls = random.randint(1, 10)
        match.home_team_corner_kicks = random.randint(1, 10)
        match.home_team_offsides = random.randint(1, 10)
        match.home_team_ball_possession = random.uniform(1, 10)
        match.home_team_yellow_cards = random.randint(1, 10)
        match.home_team_red_cards = random.randint(1, 10)
        match.home_team_goalkeeper_saves = random.randint(1, 10)
        match.home_team_total_passes = random.randint(1, 10)
        match.home_team_passes_accuracy = random.randint(1, 10)
        match.home_team_passes_percent = random.uniform(1, 10)

        match.away_team_shots_on_goal = random.randint(1, 10)
        match.away_team_shots_off_goal = random.randint(1, 10)
        match.away_team_total_shots = random.randint(1, 10)
        match.away_team_blocked_shots = random.randint(1, 10)
        match.away_team_shots_insidebox = random.randint(1, 10)
        match.away_team_shots_outsidebox = random.randint(1, 10)
        match.away_team_fouls = random.randint(1, 10)
        match.away_team_corner_kicks = random.randint(1, 10)
        match.away_team_offsides = random.randint(1, 10)
        match.away_team_ball_possession = random.uniform(1, 10)
        match.away_team_yellow_cards = random.randint(1, 10)
        match.away_team_red_cards = random.randint(1, 10)
        match.away_team_goalkeeper_saves = random.randint(1, 10)
        match.away_team_total_passes = random.randint(1, 10)
        match.away_team_passes_accuracy = random.randint(1, 10)
        match.away_team_passes_percent = random.uniform(1, 10)

        print(f"Zaktualizowano mecz {match.match_id}")
        db.session.commit()
