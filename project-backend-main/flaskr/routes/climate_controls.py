from flask import Blueprint, abort, jsonify
from ..DatabaseModels import AC_Activity, Climate_Mode, Sensors
from .. import db
from sqlalchemy import desc

from datetime import date, time, datetime
climateview = Blueprint('climateview', __name__)


@climateview.route('/get-temp', methods=['GET'])
def get_current_temp():
    '''
    Method: GET

    Returns:
        JSON: {
            "curr_temp": (int) Current temperature of the room
        }
    '''
    temp_data = AC_Activity.query.order_by(desc(AC_Activity.id)).first()
    return jsonify({
        "curr_temp": temp_data.curr_temp,
        "set_temp": temp_data.set_temp
    }), 200

@climateview.route('/get-mode', methods=['GET'])
def get_current_mode():
    '''
    Method: GET

    Returns:
        JSON: {
            "mode": (string) Mode of the climate control system
        }
    '''
    temp_data = AC_Activity.query.order_by(desc(AC_Activity.id)).first()
    return jsonify({
        "mode": temp_data.mode.name
    }), 200

@climateview.route('/change-mode/<string:mode>', methods=['POST'])
def change_mode(mode):
    '''
    Metho: POST

    Params: 
        mode: (string) Change the mode of the climate control system
        - the mode can be one of the following: "off", "ac", "heat"

    Returns:
        JSON: {
            "curr_temp": (int) Current temperature of the room,
            "set_temp": (int) Set temperature of the climate control system,
            "mode": (string) Mode of the climate control system,
            "date": (string) Date of the activity,
            "time": (string) Time of the activity,
            "watts": (int) Power consumption of the climate control system,
            "price": (float) Cost of the climate control system
        }

    Error:
        400: The mode is not one of the above
    '''

    if mode not in Climate_Mode.__members__:
        abort(400)
    
    activity = AC_Activity.query.order_by(desc(AC_Activity.id)).first()

    new_activity = AC_Activity(curr_temp=activity.curr_temp, set_temp=activity.set_temp, mode=Climate_Mode(mode), watts=0, price=0)
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        "curr_temp": new_activity.curr_temp,
        "set_temp": new_activity.set_temp,
        "mode": new_activity.mode.name,
        "date": new_activity.date.strftime("%Y-%m-%d"),
        "time": new_activity.time.strftime("%H:%M:%S"),
        "watts": new_activity.watts,
        "price": new_activity.price
    }), 200

@climateview.route('/change-temp/<int:temp>', methods=['POST'])
def change_temp(temp):
    '''
    Method: POST
    
    Parmams:
        temp: (int) Change the set temperature of the climate control system
    
    Returns:
        JSON: {
            "curr_temp": (int) Current temperature of the room,
            "set_temp": (int) Set temperature of the climate control system,
            "mode": (string) Mode of the climate control system,
            "date": (string) Date of the activity,
            "time": (string) Time of the activity,
            "watts": (int) Power consumption of the climate control system,
            "price": (float) Cost of the climate control system
        }

    Error:
        404: The temperature is not between 60 and 90 degrees
    '''
    if temp < 60 or temp > 90:
        abort(400)
    
    activity = AC_Activity.query.order_by(desc(AC_Activity.id)).first()

    new_activity = AC_Activity(curr_temp=activity.curr_temp, set_temp=temp, mode=activity.mode, watts=0, price=0)
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        "curr_temp": new_activity.curr_temp,
        "set_temp": new_activity.set_temp,
        "mode": new_activity.mode.name,
        "date": new_activity.date.strftime("%Y-%m-%d"),
        "time": new_activity.time.strftime("%H:%M:%S"),
        "watts": new_activity.watts,
        "price": new_activity.price
    }), 200

@climateview.route('/update-curr-temp/<int:temp>', methods=['POST'])
def update_curr_temp(temp):
    '''
    Method: POST

    Params:
        temp: (int) Update the current temperature of the house as the climate control system is running

    Returns:
        JSON: {
            "curr_temp": (int) Current temperature of the room,
            "set_temp": (int) Set temperature of the climate control system,
            "mode": (string) Mode of the climate control system,
            "date": (string) Date of the activity,
            "time": (string) Time of the activity,
            "watts": (int) Power consumption of the climate control system,
            "price": (float) Cost of the climate control system
        }
    '''

    activity = AC_Activity.query.order_by(desc(AC_Activity.id)).first()

    temp_diff = abs(temp - activity.curr_temp)
    watts = temp_diff * 3500/60
    price = watts * 0.12/1000

    new_activity = AC_Activity(curr_temp=temp, set_temp=activity.set_temp, mode=activity.mode, watts=watts, price=price)
    db.session.add(new_activity)
    db.session.commit()

    return jsonify({
        "curr_temp": new_activity.curr_temp,
        "set_temp": new_activity.set_temp,
        "mode": new_activity.mode.name,
        "date": new_activity.date.strftime("%Y-%m-%d"),
        "time": new_activity.time.strftime("%H:%M:%S"),
        "watts": new_activity.watts,
        "price": new_activity.price
    }), 200