# from app.controllers.airlineController import *
from flask import blueprints
from flask import Flask, jsonify
from app.models.user import User
from app.models.season import Season
import requests
airlinebp = blueprints.Blueprint('airlinebp', __name__)
API_KEY = 'e1585dfda852e31d5849162cb7a24b24'
BASE_URL = 'https://v3.football.api-sports.io'

# Endpoint do wyświetlania 10 najlepszych strzelców ligi Premier League
@airlinebp.route('/topscorers', methods=['GET'])
def topscorers():
    url = f'{BASE_URL}/players/topscorers?league=39&season=2024'
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Endpoint do wyświetlania 10 najlepszych asystentów ligi Premier League
@airlinebp.route('/topassists', methods=['GET'])
def topassists():
    url = f'{BASE_URL}/players/topassists?league=39&season=2024'
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Endpoint do wyświetlenia każdej drużyny z danego sezonu z każdej ligi którą mam w bazie
@airlinebp.route('/teams', methods=['GET'])
def teams():
    url = f'{BASE_URL}/teams?league=39&season=2024'
    headers = {
        'x-rapidapi-key': API_KEY,  
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(url, headers=headers)
    return response.json()

@airlinebp.route('/teams', methods=['GET'])
def get_teams():
    url = 'https://v3.football.api-sports.io/teams'
    headers = {
        'x-rapidapi-key': API_KEY
    }
    params = {
        'league': 39,  # Premier League
        'season': 2021
    }
    
    # Wysłanie zapytania do API
    response = requests.get(url, headers=headers, params=params)
    
    # Sprawdzenie czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        return jsonify(response.json())  # Zwracamy odpowiedź jako JSON
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code

@airlinebp.route('/statistics', methods=['GET'])
def get_teams_statistics():
    url = 'https://v3.football.api-sports.io/teams/statistics'
    headers = {
        'x-rapidapi-key': API_KEY
    }
    params = {
        'team': 33,
        'league': 39,  # Premier League
        'season': 2021
    }
    
    # Wysłanie zapytania do API
    response = requests.get(url, headers=headers, params=params)
    


    
    # Sprawdzenie czy zapytanie zakończyło się sukcesem
    if response.status_code == 200:
        return jsonify(response.json())  # Zwracamy odpowiedź jako JSON
    else:
        return jsonify({'error': 'Failed to fetch data'}), response.status_code





def get_upcoming_matches():
    url = f'{BASE_URL}/fixtures?league=39&season=2024&next=10'  # 39 to ID Premier League, "next=10" pobiera 10 kolejnych meczów
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': 'v3.football.api-sports.io'
    }
    response = requests.get(url, headers=headers)
    return response.json()




def get_league_coverage():
    seasons = Season.query.all()
    for season in seasons:
        url = f'{BASE_URL}/leagues?id=39&season={season.name}'
        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
    return None

# Endpoint do wyświetlania coverage dla Premier League
@airlinebp.route('/coverage', methods=['GET'])
def coverage():
    coverage_data = get_league_coverage()
    
    if coverage_data:
        return jsonify(coverage_data)
    else:
        return jsonify({"error": "Unable to fetch coverage data"}), 500

@airlinebp.route("/airlines", methods=["GET"])
def hello():
    return "Hello, World!"

@airlinebp.route("/user", methods=["get"])
def get_users():
    users = User.query.all()

    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])

@airlinebp.route('/upcoming', methods=['GET'])
def upcoming_matches():
    data = get_upcoming_matches()
    
    matches = []
    for match in data['response']:
        fixture = match['fixture']
        home_team = match['teams']['home']['name']
        away_team = match['teams']['away']['name']
        match_date = fixture['date']
        
        matches.append({
            'home_team': home_team,
            'away_team': away_team,
            'date': match_date
        })
    
    return jsonify(matches)

@airlinebp.route('/reload', methods=['GET'])  
def reload():
    return "Reloaded"