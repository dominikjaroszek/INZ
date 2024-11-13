# controllers.py
from flask import Blueprint, jsonify, abort
from app.services.matchService import *


match_bp = Blueprint('matches', __name__)

@match_bp.route('/upcoming-matches/round', methods=['GET'])
def upcoming_round():
    matches_by_league = get_upcoming_rounds()
    return jsonify(matches_by_league)

@match_bp.route('/upcoming-matches/<string:league_name>/<string:season>/<int:limit>', methods=['GET'])
def upcoming_matches_by_league(league_name, limit, season):
    if season == '2024-2025':
        matches_list = get_upcoming_matches_by_league(league_name, limit)
    else:
        return jsonify({'data': 'Nie ma nadchodzacch meczów dla podanego sezonu'})
    if not matches_list:
        abort(404, description="No matches found for the given league or limit.")
    return jsonify(matches_list)

@match_bp.route('/finished-matches/round', methods=['GET'])
def finished_round():
    matches_by_league = get_finished_rounds_by_league()
    if not matches_by_league:
        abort(404, description="No finished matches found.")
    return jsonify(matches_by_league)

# Endpoint dla zakończonych meczów w danej lidze
@match_bp.route('/finished-matches/<string:league_name>/<string:season_name>/<int:limit>', methods=['GET'])
def finished_matches_by_league(league_name, limit, season_name):
    matches_list = get_finished_matches_by_league(league_name, limit, season_name)
    if not matches_list:
        abort(404, description="No matches found for the given league or limit.")
    return jsonify(matches_list)

# Endpoint do meczów live z danej ligi
@match_bp.route('/live/<string:league_name>', methods=['GET'])
def live_matches_by_league(league_name):
    matches_list = get_live_matches_by_league(league_name)
    if not matches_list:
        return jsonify({})
    return jsonify(matches_list)


#Endpoint do szczegółów meczu
@match_bp.route('/match/<int:match_id>', methods=['GET'])
def match_details(match_id):
    match = get_match_by_id(match_id)
    if not match:
        abort(404, description="No match found for the given id.")
    return jsonify(match)

@match_bp.route('/live', methods=['GET'])
def live_matches():
    matches_list = get_live_all_matches()
    return jsonify(matches_list)