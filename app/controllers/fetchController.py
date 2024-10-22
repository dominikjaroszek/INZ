from flask import blueprints
from flask import jsonify
from app.services.fetchService import *

fetch_bp = blueprints.Blueprint('fetchbp', __name__)

@fetch_bp.route('/leagues', methods=['GET'])
def leagues():
    update_all_data()
    return jsonify(1)