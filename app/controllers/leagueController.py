from flask import blueprints
from flask import Flask, jsonify
from app.models.league import League
from app.services.leagueService import *

leaguebp = blueprints.Blueprint('leaguebp', __name__)

@leaguebp.route('/leagues', methods=['GET'])
def leagues():
    return jsonify(get_league_coverage())