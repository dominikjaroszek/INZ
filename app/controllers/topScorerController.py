from flask import blueprints
from flask import jsonify
from app.services.topScorerService import *

topScorer_bp = blueprints.Blueprint('topScorer', __name__)

@topScorer_bp.route('/leagues/top_scorers/<string:league_name>/<string:season>', methods=['GET'])
def top_scorers(league_name, season):
    top_scorers = get_top_scorers(league_name, season)
    return jsonify(top_scorers)

@topScorer_bp.route('/leagues/top_scorers_canadian/<string:league_name>/<string:season>', methods=['GET'])
def top_scorers_canadian(league_name, season):
    top_scorers = get_top_scorers_canadian(league_name, season)
    return jsonify(top_scorers)