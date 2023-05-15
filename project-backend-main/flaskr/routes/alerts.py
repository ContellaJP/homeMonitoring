from flask import Blueprint, request, jsonify

from ..DatabaseModels import Sensors, Sensor_Type, AC_Activity, Activity, Climate_Mode
from .. import db


alertview = Blueprint('alertview', __name__)

@alertview.route('/alerts', methods=["POST"])
def home():
    
    return jsonify({
        "alerts": ["Backdoor open", "Garagedoor open"],
        }), 200