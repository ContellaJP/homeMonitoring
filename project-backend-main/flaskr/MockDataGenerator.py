from . import db
from .DatabaseModels import Sensor_Type, Sensors, AC_Activity, Activity, Climate_Mode

def generate_bedroom_sensor_data():
    bedrooms = ['master-bedroom', 'bedroom-2', 'bedroom-3']
    for br in bedrooms:
        #lights
        sensor = Sensors(sensor_type=Sensor_Type.light, room=br, name='overhead', status=0)
        db.session.add(sensor)

        sensor = Sensors(sensor_type=Sensor_Type.light, room=br, name='lamp 1', status=0)
        db.session.add(sensor)

        sensor = Sensors(sensor_type=Sensor_Type.light, room=br, name='lamp 2', status=0)
        db.session.add(sensor)

        # windows
        sensor = Sensors(sensor_type=Sensor_Type.window, room=br, name='window 1', status=0)
        db.session.add(sensor)

        sensor = Sensors(sensor_type=Sensor_Type.window, room=br, name='window 2', status=0)
        db.session.add(sensor)

    # outlets
    sensor = Sensors(sensor_type=Sensor_Type.outlet, room='master-bedroom', name='television', status=0)
    db.session.add(sensor)

    db.session.commit()

def generate_bathroom_sensor_data():
    bathrooms = ['master-bathroom', 'hall-bathroom']
    for br in bathrooms:
        #lights
        sensor = Sensors(sensor_type=Sensor_Type.light, room=br, name='overhead', status=0)
        db.session.add(sensor)

        #windows
        sensor = Sensors(sensor_type=Sensor_Type.window, room=br, name='window', status=0)
        db.session.add(sensor)

        #outlets
        sensor = Sensors(sensor_type=Sensor_Type.outlet, room=br, name='fan', status=0)
        db.session.add(sensor)

        #water
        sensor = Sensors(sensor_type=Sensor_Type.water, room=br, name='bathtub', status=0)
        db.session.add(sensor)

        sensor = Sensors(sensor_type=Sensor_Type.water, room=br, name='sink', status=0)
        db.session.add(sensor)

    db.session.commit()

def generate_garage_sensor_data():
    #lights
    sensor = Sensors(sensor_type=Sensor_Type.light, room='garage', name='overhead', status=0)
    db.session.add(sensor)

    #doors
    sensor = Sensors(sensor_type=Sensor_Type.door, room='garage', name='garage exterior door', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.door, room='garage', name='garage door 1', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.door, room='garage', name='garage door 2', status=0)
    db.session.add(sensor)

    #appliances
    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='garage', name='water heater', status=0)
    db.session.add(sensor)

    db.session.commit()

def generate_landry_sensor_data():
    #appliances
    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='laundry', name='washer', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='laundry', name='dryer', status=0)
    db.session.add(sensor)

    #lights
    sensor = Sensors(sensor_type=Sensor_Type.light, room='laundry', name='overhead', status=0)
    db.session.add(sensor)

    db.session.commit()

def generate_livingroom_sensor_data():
    #lights
    sensor = Sensors(sensor_type=Sensor_Type.light, room='living-room', name='overhead', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.light, room='living-room', name='lamp 1', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.light, room='living-room', name='lamp 2', status=0)
    db.session.add(sensor)
    

    # windows
    sensor = Sensors(sensor_type=Sensor_Type.window, room='living-room', name='window 1', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.window, room='living-room', name='window 2', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.window, room='living-room', name='window 3', status=0)
    db.session.add(sensor)

    # outlets
    sensor = Sensors(sensor_type=Sensor_Type.outlet, room='living-room', name='television', status=0)
    db.session.add(sensor)

    #doors
    sensor = Sensors(sensor_type=Sensor_Type.door, room='living-room', name='backdoor', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.door, room='living-room', name='frontdoor', status=0)
    db.session.add(sensor)

    db.session.commit()

def generate_kitchen_sensor_data():
    #lights
    sensor = Sensors(sensor_type=Sensor_Type.light, room='kitchen', name='overhead', status=0)
    db.session.add(sensor)

    #appliances
    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='kitchen', name='oven', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='kitchen', name='stove', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='kitchen', name='dishwasher', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='kitchen', name='fridge', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.appliance, room='kitchen', name='microwave', status=0)
    db.session.add(sensor)

    # windows
    sensor = Sensors(sensor_type=Sensor_Type.window, room='kitchen', name='window 1', status=0)
    db.session.add(sensor)

    sensor = Sensors(sensor_type=Sensor_Type.window, room='kitchen', name='window 2', status=0)
    db.session.add(sensor)

    #water
    sensor = Sensors(sensor_type=Sensor_Type.water, room='kitchen', name='sink', status=0)
    db.session.add(sensor)
    
    db.session.commit()
    
def MakeMockData():
    generate_bedroom_sensor_data()
    generate_bathroom_sensor_data()
    generate_garage_sensor_data()
    generate_landry_sensor_data()
    generate_livingroom_sensor_data()
    generate_kitchen_sensor_data()