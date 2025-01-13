
from flask import blueprints
from flask import jsonify
from app.services.apiService import *

api_bp = blueprints.Blueprint('apibp', __name__)

@api_bp.route('/update_statists_back', methods=['GET'])
def update_statists_back():
   update_match_details_back(39)
   update_match_details_back(140)

@api_bp.route('/update_standing_form', methods=['GET'])
def update_standing_form_controller():
   update_standing_form()


@api_bp.route('/update_wskazniki', methods=['GET'])
def update_wskazniki_controller():
   update_wskazniki(39)
   update_wskazniki(140)

@api_bp.route('/update_statists_back_test', methods=['GET'])
def update_statists_back_test():
   update_match_details_back_test(39)
   update_match_details_back_test(140)



@api_bp.route('/check_update', methods=['GET'])
def check_update_controller():
   check_update(39)
   check_update(140)