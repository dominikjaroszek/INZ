from flask import blueprints
from flask import Flask, jsonify
from app.services.leagueService import *

league_bp = blueprints.Blueprint('leaguebp', __name__)

@league_bp.route('/leagues', methods=['GET'])
def leagues():
    update_all_data()
    return jsonify(1)


@league_bp.route('/leagues/names', methods=['GET'])
def get_leagues():
    league_names = get_all_league_names()
    return jsonify(league_names)    