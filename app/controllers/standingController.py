from flask import blueprints
from flask import jsonify
from app.services.standingService import *

standing_bp = blueprints.Blueprint('standing', __name__)

@standing_bp.route('/leagues/standings/<string:league_name>/<string:season>', methods=['GET'])
def standings(league_name, season):
    standings = get_standings(league_name, season)
    return jsonify(standings)

@standing_bp.route('/leagues/standings/home/<string:league_name>/<string:season>', methods=['GET'])
def standings_home(league_name, season):
    standings = get_standings_home(league_name, season)
    return jsonify(standings)

@standing_bp.route('/leagues/standings/away/<string:league_name>/<string:season>', methods=['GET'])
def standings_away(league_name, season):
    standings = get_standings_away(league_name, season)
    return jsonify(standings)