from flask import blueprints
from flask import jsonify
from app.services.leagueService import *

league_bp = blueprints.Blueprint('leaguebp', __name__)

@league_bp.route('/leagues/names', methods=['GET'])
def get_leagues():
    league_names = get_all_league_names()
    return jsonify(league_names)    

@league_bp.route('/leagues/<string:league_name>/<string:season>', methods=['GET'])
def league(league_name,season):
    league = get_league(league_name, season)
    return jsonify(league)

@league_bp.route('/leagues/<string:league_name>/seasons', methods=['GET'])
def get_seasons(league_name):
    seasons = get_all_seasons(league_name)
    return jsonify(seasons)