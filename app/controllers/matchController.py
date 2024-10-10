# controllers.py
from flask import Blueprint, jsonify, abort
from app.services.matchService import *


match_bp = Blueprint('matches', __name__)

@match_bp.route('/upcoming-matches/round', methods=['GET'])
def upcoming_round():
    matches_by_league = get_upcoming_round()
    return jsonify(matches_by_league)

@match_bp.route('/upcoming-matches/<string:league_name>/<int:limit>', methods=['GET'])
def upcoming_matches_by_league(league_name, limit):
    matches_list = get_upcoming_matches_by_league(league_name, limit)
    if not matches_list:
        abort(404, description="No matches found for the given league or limit.")
    return jsonify(matches_list)

@match_bp.route('/finished-matches/round', methods=['GET'])
def finished_round():
    matches_by_league = get_finished_round()
    if not matches_by_league:
        abort(404, description="No finished matches found.")
    return jsonify(matches_by_league)

# Endpoint dla zakończonych meczów w danej lidze
@match_bp.route('/finished-matches/<string:league_name>/<int:limit>', methods=['GET'])
def finished_matches_by_league(league_name, limit):
    matches_list = get_finished_matches_by_league(league_name, limit)
    if not matches_list:
        abort(404, description="No matches found for the given league or limit.")
    return jsonify(matches_list)