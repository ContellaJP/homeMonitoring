import enum
from . import db
from sqlalchemy import Enum, Date, Time, Integer, String, ForeignKey, Float, Column
from datetime import datetime

class Sensor_Type(enum.Enum):
    '''
    Sensor_type: door, window, light, water, outlet, appliance
    '''
    door = 'door'
    window = 'window'
    light = 'light'
    water = 'water'
    outlet = 'outlet'
    appliance = 'appliance'


class Climate_Mode(enum.Enum):
    '''
    Climate_Mode: ac, heat, off
    '''
    ac = 'ac'
    heat = 'heat'
    off = 'off'


class Sensors(db.Model):
    '''
    sensor_id: (integer) unique id for each sensor
    sensor_type: (Sensor_Type) type of sensor
    room: (string) room the sensor is in
    name: (string) name of the sensor
    status: (integer) 0 or 1, 0 is off, 1 is on
    '''
    __tablename__ = "sensors"
    sensor_id = Column(Integer, primary_key=True)
    sensor_type = Column(Enum(Sensor_Type), nullable=False)
    room = Column(String(32), nullable=False)
    name = Column(String(32), nullable=False)
    status = Column(Integer, nullable=False)


class Activity(db.Model):
    '''
    activity_id: (integer) unique id for each activity
    sensor_id: (integer) id of the sensor that was used
    start_date: (date) date the activity started
    start_time: (time) time the activity started
    watt_consumption: (integer) watts used over the duration
    water_consumption: (integer) gallons used over the duration
    power_price: (float) cost of power over the duration
    water_price: (float) cost of water over the duration
    duration: (float) duration of the activity in hours
    '''
    __tablename__ = "activity"
    activity_id = Column(Integer, primary_key=True)
    sensor_id = Column(ForeignKey('sensors.sensor_id'), nullable=False)
    start_date = Column(Date, nullable=False, default=datetime.now().date().strftime("%Y-%m-%d"))
    start_time = Column(Time, nullable=False, default=datetime.now().time().strftime("%H:%M:%S"))
    watt_consumption = Column(Float, nullable=False, default=0)
    water_consumption = Column(Float, nullable=False, default=0)
    power_price = Column(Float, nullable=False, default=0)
    water_price = Column(Float, nullable=False, default=0)
    duration = Column(Float, nullable=False, default=0)


class AC_Activity(db.Model):
    '''
    curr_temp: (integer) interior temperature
    set_temp: (integer) temperature the thermostat is set at
    mode: 'ac', 'heat', 'off'
    date: date of recording
    time: time of recording
    watts: (float) watts used since last record
    price: (float) cost accumulated since last record
    '''
    __tablename__ = "ac_activity"
    id = Column(Integer, primary_key=True)
    curr_temp = Column(Integer, nullable=False)
    set_temp = Column(Integer, nullable=False)
    mode = Column(Enum(Climate_Mode), nullable=False)
    date = Column(Date, nullable=False, default=datetime.now().date().strftime("%Y-%m-%d"))
    time = Column(Time, nullable=False, default=datetime.now().time().strftime("%H:%M:%S"))
    watts = Column(Float, nullable=False)
    price = Column(Float, nullable=False)