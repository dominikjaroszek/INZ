from app.services.teamService import *
from flask import blueprints
from flask import jsonify
from flask import request

team_bp = blueprints.Blueprint('team', __name__)

@team_bp.route('/team/<string:team_name>', methods=['GET'])
def get_team_by_name(team_name):
    team = get_team(team_name)
    return jsonify(team)        

@team_bp.route('/team/<string:team_name>/finished/<int:limit>', methods=['GET'])
def get_team_matches_finished(team_name, limit):
    matches = get_finished_matches(team_name, limit)
    return jsonify(matches)

@team_bp.route('/team/<string:team_name>/upcoming/<int:limit>', methods=['GET'])
def get_team_matches_upcoming(team_name, limit):
    matches = get_upcoming_matches(team_name, limit)
    return jsonify(matches)

@team_bp.route('/team/<string:team_name>/live', methods=['GET'])
def get_team_match_live(team_name):
    matches = get_live_match(team_name)
    return jsonify(matches)

@team_bp.route('/search', methods=['GET'])
def search_teams():
    value = request.args.get('q')
    teams = search_team(value)
    return jsonify(teams)