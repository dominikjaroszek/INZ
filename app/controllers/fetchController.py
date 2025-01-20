from flask import blueprints
from flask import jsonify
from app.services.fetchService import *
from app.services.apiService import *

fetch_bp = blueprints.Blueprint('fetchbp', __name__)

@fetch_bp.route('/leagues', methods=['GET'])
def leagues():
    update_all_data()
    return jsonify(1)

@fetch_bp.route('/match-details', methods=['GET'])
def match_details():
    update_match_details_back(39)
    return jsonify(1)