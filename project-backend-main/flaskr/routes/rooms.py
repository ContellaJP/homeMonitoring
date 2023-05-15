from flask import Blueprint, request, jsonify
from .. import db
from ..DatabaseModels import Sensors

devices = Blueprint('devices', __name__)

@devices.route('/rooms-list-status', methods=["POST"])
def rooms_list():
    '''
    Method: POST

    Returns: 
        JSON: {
            "rooms": [
                "room1",
                "room2",
            ... ],
            "room1": {
                "device1": {
                    "status": (int) Status of the device,
                    "id": (int) ID of the device,
                    "type": (string) Type of the device
                },  
                "device2": {
                    "status": (int) Status of the device,
                    "id": (int) ID of the device,   
                    "type": (string) Type of the device
                },
            ... },
            ...
        }
    '''
    rooms = Sensors.query.with_entities(Sensors.room).distinct().all()

    response = {}

    room_list = []
    for room in rooms:
        room_list.append(room.room)
    response["rooms"] = room_list

    
    for room in room_list:
        devices = Sensors.query.filter_by(room=room).all()
        device_list_statuss = {}
        for device in devices:
            device_list_statuss[device.name] = {
                "status": device.status,
                "id": device.sensor_id,
                "type": device.sensor_type.name
            }
        response[room] = device_list_statuss
    
    return jsonify(response), 200