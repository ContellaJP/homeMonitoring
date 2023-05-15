from flask import Blueprint, request, jsonify, abort
from .. import db
from ..DatabaseModels import Sensors, Activity, Sensor_Type
from datetime import datetime
from sqlalchemy import desc


sensor_updates = Blueprint('doors', __name__)

@sensor_updates.route('/door-state-change/<int:id>', methods=['POST'])
def door_state_change(id):
    '''
    Params:
        id: (int) Change the state of the door sensor with id

    Returns:
        JSON: {
            "door": (int) ID of the door sensor,
            "status": (int) Status of the door sensor
        }

    Error:
        404: Sensor with id does not exist or is not a door sensor
    '''
    door = Sensors.query.filter_by(sensor_id=id).first()

    if door is None:    
        abort(404)
    if door.sensor_type != Sensor_Type.door:
        abort(400)
    
    if door.status == 0:
        db.session.add(Activity(sensor_id=id))

    elif door.status == 1:
        activity = Activity.query.filter_by(sensor_id=id).order_by(desc(Activity.activity_id)).first()
        start_datetime = datetime.combine(activity.start_date, activity.start_time)
        activity.duration = (datetime.now() - start_datetime).total_seconds() / 60
    
    door.status = (1 - door.status)
    db.session.commit()
    return jsonify({"door": id, "status": door.status,}), 200


@sensor_updates.route('/window-state-change/<int:id>', methods=['POST'])
def window_state_change(id):
    '''
    Params:
        id: (int) Change the state of the window sensor with id

    Returns:
        JSON: {
            "window": (int) ID of the window sensor,
            "status": (int) Status of the window sensor
        }

    Error:
        404: Sensor with id does not exist or is not a window sensor
    '''
    window = Sensors.query.filter_by(sensor_id=id).first()

    if window is None:    
        abort(404)
    if window.sensor_type != Sensor_Type.window:
        abort(400)

    if window.status == 0:
        db.session.add(Activity(sensor_id=id))

    elif window.status == 1:
        activity = Activity.query.filter_by(sensor_id=id).order_by(desc(Activity.activity_id)).first()
        start_datetime = datetime.combine(activity.start_date, activity.start_time)
        activity.duration = (datetime.now() - start_datetime).total_seconds() / 60
    
    window.status = (1 - window.status)
    db.session.commit()
    return jsonify({"window": id, "status": window.status,}), 200


@sensor_updates.route('/light-state-change/<int:id>', methods=['POST'])
def light_state_change(id):
    '''
    Params:
        id: (int) Change the state of the light sensor with id

    Returns:
        JSON: {
            "light": (int) ID of the light sensor,
            "status": (int) Status of the light sensor
        }

    Error:
        404: Sensor with id does not exist or is not a light sensor
    '''
    light = Sensors.query.filter_by(sensor_id=id).first()

    if light is None:    
        abort(404)
    if light.sensor_type != Sensor_Type.light:
        abort(400)

    if light.status == 0:
        db.session.add(Activity(sensor_id=id))

    elif light.status == 1:
        activity = Activity.query.filter_by(sensor_id=id).order_by(desc(Activity.activity_id)).first()
        start_datetime = datetime.combine(activity.start_date, activity.start_time)
        activity.duration = (datetime.now() - start_datetime).total_seconds() / 60
        activity.watt_consumption = activity.duration
        activity.power_price = activity.watt_consumption * 0.001 * .12
    
    light.status = (1 - light.status)
    db.session.commit()
    return jsonify({"light": id, "status": light.status,}), 200


@sensor_updates.route('/fan-state-change/<int:id>', methods=['POST'])
def fan_state_change(id):
    '''
    Params:
        id: (int) Change the state of the fan sensor with id

    Returns:
        JSON: {
            "fan": (int) ID of the fan sensor,
            "status": (int) Status of the fan sensor
        }

    Error:
        404: Sensor with id does not exist
        400: Sensor is not a fan sensor
    '''
    fan = Sensors.query.filter_by(sensor_id=id).first()

    if fan is None:    
        abort(404)
    if fan.sensor_type != Sensor_Type.outlet:
        abort(400)

    if fan.status == 0:
        db.session.add(Activity(sensor_id=id))

    elif fan.status == 1:
        activity = Activity.query.filter_by(sensor_id=id).order_by(desc(Activity.activity_id)).first()
        start_datetime = datetime.combine(activity.start_date, activity.start_time)
        activity.duration = (datetime.now() - start_datetime).total_seconds() / 60
        activity.watt_consumption = activity.duration / 2
        activity.power_price = activity.watt_consumption * 0.001 * .12
    
    fan.status = (1 - fan.status)
    db.session.commit()
    return jsonify({"fan": id, "status": fan.status,}), 200

@sensor_updates.route('/tv-state-change/<int:id>', methods=['POST'])
def tv_state_change(id):
    '''
    Params:
        id: (int) Change the state of the tv sensor with id

    Returns:
        JSON: {
            "tv": (int) ID of the tv sensor,
            "status": (int) Status of the tv sensor
        }

    Error:
        404: Sensor with id does not exist
        400: Sensor is not an outlet sensor
    '''
    tv = Sensors.query.filter_by(sensor_id=id).first()

    if tv is None:    
        abort(404)
    if tv.sensor_type != Sensor_Type.outlet:
        abort(400)

    if tv.status == 0:
        db.session.add(Activity(sensor_id=id))

    elif tv.status == 1:
        if tv.room =="living-room":
            watts = 636
        elif tv.room == "master-bedroom":
            watts = 100
        else:
            watts = 100
        activity = Activity.query.filter_by(sensor_id=id).order_by(desc(Activity.activity_id)).first()
        start_datetime = datetime.combine(activity.start_date, activity.start_time)
        activity.duration = (datetime.now() - start_datetime).total_seconds() / 60
        activity.watt_consumption = (activity.duration / 60) * watts
        activity.power_price = activity.watt_consumption * 0.001 * .12
    
    tv.status = (1 - tv.status)
    db.session.commit()
    return jsonify({"tv": id, "status": tv.status,}), 200


@sensor_updates.route('/hot-water-used/<int:gallons>', methods=['POST'])
def hot_water_used(gallons):
    '''
    Params:
        gallons: (int) Number of gallons used

    Returns:
        JSON: {
            "heater": (int) ID of the water heater sensor,
            "gallons": (int) Number of gallons used,
            "watt_consumption": (int) Number of watts used,
            "water_price": (float) Price of water used
        }

    Error:
        400: Gallons is less than 0
    '''
    if gallons < 0:
        abort(400)
    water_hearter = Sensors.query.filter_by(sensor_id=31).first()
    
    water_price = (2.52 / 748) * gallons
    reheat_time = (4 * gallons)
    watt_consumption = (reheat_time / 60) * 4500 
    watt_price = watt_consumption * 0.001 * .12

    db.session.add(Activity(sensor_id=31, watt_consumption=watt_consumption, water_consumption=gallons, power_price=watt_price, water_price=water_price, duration=reheat_time))
    db.session.commit()

    return jsonify({
        "heater": water_hearter.sensor_id,
        "gallons": gallons, 
        "watt_consumption": watt_consumption, 
        "water_price": water_price, 
        "watt_price": watt_price, 
        "duraion": reheat_time}), 200


@sensor_updates.route('/bath-shower-taken/<string:type>/<int:id>', methods=['POST'])
def bath_taken(type, id):
    '''
    Params:
        type: (string) "bath" or "shower"
        id: (int) Sensor id of the bath/shower sensor
        
    Returns:
        JSON: {
            "bath": (int) ID of the bath/shower sensor,
            "gallons": (int) Number of gallons used,
            "water_price": (float) Price of water used
        }
        
    Error:
        404: Sensor with id does not exist
        400: Sensor is not a water sensor
    '''
    bath = Sensors.query.filter_by(sensor_id=id).first()
    if bath is None:    
        abort(404)
    if bath.sensor_type != Sensor_Type.water:
        abort(400)

    if type == "bath":
        gallons = 30
    elif type == "shower":
        gallons = 15
    else:
        abort(400)

    cold_gallons = gallons * .65
    water_price = (2.52 / 748) * gallons
    db.session.add(Activity(sensor_id=id, water_consumption=cold_gallons, water_price=water_price))
    db.session.commit()

    hot_water_used(gallons * .35)

    return jsonify({"bath": id, "gallons": gallons, "water_price": water_price}), 200


@sensor_updates.route('/appliance-used/<string:type>/<int:id>', methods=['POST'])
def appliance_used(type, id):
    '''
    Params:
        type: (string) "fridge", "microwave", "stove", "oven", "dishwasher", "washer"
        id: (int) Sensor id of the appliance sensor
        
    Returns:
        JSON: {
            "appliance": (int) ID of the appliance sensor,
            "duration": (int) Duration of appliance use in minutes,
            "watt_consumption": (int) Number of watts used,
            "power_price": (float) Price of power used
        }
        
    Error:
        404: Sensor with id does not exist
        400: Sensor is not an appliance sensor
    '''
    appliance = Sensors.query.filter_by(sensor_id=id).first()
    if appliance is None:    
        abort(404)
    if appliance.sensor_type != Sensor_Type.appliance:
        abort(400)

    water_consumption = 0
    if type == "fridge":
        duration = 60
        watt_consumption = 150
    elif type == "microwave":
        duration = 1
        watt_consumption = (duration / 60) * 1100
    elif type == "stove":
        duration = 15
        watt_consumption = (duration / 60) * 3500
    elif type == "oven":
        duration = 15
        watt_consumption = (duration / 60) * 4000
    elif type == "dishwasher":
        duration = 45
        watt_consumption = (duration / 60) * 1800
        hot_water_used(6)
    elif type == "washer":
        duration = 30
        watt_consumption = (duration / 60) * 500
        water_consumption = 20 
        hot_water_used(water_consumption * 0.85)
        water_consumption = water_consumption * 0.15
    elif type == "dryer":
        duration = 30
        watt_consumption = (duration / 60) * 3000
    else:
        abort(400)

    watt_price = watt_consumption * 0.001 * .12
    water_price = (2.52 / 748) * water_consumption
    db.session.add(Activity(sensor_id=id, duration=duration, watt_consumption=watt_consumption, water_consumption=water_consumption, power_price=watt_price, water_price=water_price))
    db.session.commit()

    return jsonify({"appliance": id, "duration": duration, "watt_consumption": watt_consumption, "water_consumption": water_consumption, 
                        "watt_price": watt_price, "water_price": water_price}), 200


