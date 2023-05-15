from flask import Blueprint, jsonify, abort
from ..DatabaseModels import AC_Activity, Activity
from .. import db 
from sqlalchemy import func, cast, String
from datetime import datetime
utilities = Blueprint('utilities', __name__)

@utilities.route('/utility-history-cost/<period>/<string:date>', methods=['GET', 'POST'])
def utilitycost(period, date):
    '''
    Serves historic utility usage data to client based on specified period.

    Request Types: POST

    Path: 
        "/utility-cost/<period>/<date>"
        period is a wild card and will serve data based on the period provided.

        Valid Periods:
            - hourly: hourly break down for current day's power usage, up to current hour.
            - daily: daily break down for current week's power usage, up to current day.

        Valid Dates:
            - YYYY-MM-DD: date to start from. If date is not provided, data will start from the beginning of time.

    Returns:
        JSON: { 
                period: start to end period of data provided,
                period : {
                    power: power consumption over this period,
                    water: water consumption over this period,
                    power-cost: cost of power,
                    water-cost: cost of water
                },
                total-power-cost: cost of power over entire time period,
                total-water-cost: cost of water over entire time period
            }
        
    Error:
        404: Invalid period provided
        400: Invalid date provided
    '''
    if period not in ["hourly", "daily"]:
        abort(404)
    if date is not None and not _is_valid_date(date): 
        abort(400)

    given_date = datetime.strptime(date, "%Y-%m-%d")
    activities = Activity.query.all()
    
    if _is_valid_date(date): 
        activities = [activity for activity in activities if activity.start_date >= given_date.date()]
    
    history = {}
    watts, gallons, power_cost, water_cost = 0, 0, 0, 0
    for activity in activities:
        period_data = {
            "watts" : 0,
            "gallons" : 0,
            "power-cost" : 0,
            "water-cost" : 0
        }
        watts += activity.watt_consumption
        gallons += activity.water_consumption
        power_cost += activity.power_price
        water_cost += activity.water_price

        
        if period == "hourly":
            formatted_date_time = activity.start_date.strftime("%Y-%m-%d") + " " + activity.start_time.strftime("%H:%M:%S")
            if formatted_date_time not in history:
                history[formatted_date_time] = period_data
            history[formatted_date_time]["watts"] += activity.watt_consumption
            history[formatted_date_time]["gallons"] += activity.water_consumption
            history[formatted_date_time]["power-cost"] += activity.power_price
            history[formatted_date_time]["water-cost"] += activity.water_price

        elif period == "daily":
            formatted_date = activity.start_date.strftime("%Y-%m-%d")
            if formatted_date not in history:
                history[formatted_date] = period_data
            history[formatted_date]["watts"] += activity.watt_consumption
            history[formatted_date]["gallons"] += activity.water_consumption
            history[formatted_date]["power-cost"] += activity.power_price
            history[formatted_date]["water-cost"] += activity.water_price

    return jsonify({
        "periods" : list(history.keys()),
        "history" : history,
        "total-watts" : watts,
        "total-gallons" : gallons,
        "total-power-cost" : power_cost,
        "total-water-cost" : water_cost
    }), 200


@utilities.route('/utility-estimate/<period>', methods=['POST'])
def utility_estimate(period):
    '''
    Serves estimated utility usage data to client. This data is calculated based on
    historic utility average use. 

    Request Type: Post
    Path: 
        "/utility-estimate/<period>"
        period is a wild card and will serve data based on the period provided.

        Valid Periods:
            - hourly: estimate for each hour over a 24 hour time period
            - daily: estimate for each day over 1 week period
            - weekly: estimate for each week over 3 months
            - monthly: estimate for each month over 12 monh for cast (ex may 2023 - april 2024)
    Returns:
        JSON: { 
                period: start to end period of data provided,
                estimate : {
                    power-est: estimate of power consumption over this period,
                    water-est: estimate of water consumption over this period,
                    power-cost-est: cost of power estimate,
                    water-cost-est: cost of water estimate
                }
                total-power-cost: cost of power over entire time period,
                total-water-cost: cost of water over entire time period
            }
        
    '''
    power_cost, water_cost = 0, 0

    if period == "hourly":
        estimate = {
            "01:00:00" : {
                "power-est": 150,
                "water-est" : 0,
                "power-cost-est" :  15,
                "water-cost-est" : 20
            }
        }
    elif period == "daily":
        estimate = {
            "01-01-2023" : {
                "power-est": 150,
                "water-est" : 0,
                "power-cost-est" :  15,
                "water-cost-est" : 20
            }
        }
    elif period == "weekly":
        estimate = {
            "01-01-2023p" : {
                "power-est": 150,
                "water-est" : 0,
                "power-cost-est" :  15,
                "water-cost-est" : 20
            }
        }
    elif period == "monthly":
        estimate = {
            "01" : {
                "power-est": 150,
                "water-est" : 0,
                "power-cost-est" :  15,
                "water-cost-est" : 20
            }
        }
    else: abort(404)
    
    return jsonify({
        "period" : period,
        "estimate" : estimate,
        "total-power-cost" : power_cost,
        "total-water-cost" : water_cost
    })



#Basic overview/thought process for this approach-
#There will be a space in the DB containing the % change between our current price and the new adjusted price
#"pastyears" is amount of years between the selected year of inflation and our current year
#"modifier" simply is the % change variable
#"modifiedValue" is the value that has been adjusted by inflation returned from backend

@utilities.route('/inflation-calculator/<pastyears>', methods=['GET','POST'])
def inflation_calculator(pastyears):
    if pastyears == "5":
        inflation = {
            "modifier" : .0244,
            "modifiedValue" : 42030
    }
    elif pastyears == "10":
        inflation = {
            "modifier" : .0123,
            "modifiedValue" : 40142
    }
    elif pastyears == "20":
        inflation = {
            "modifier" : .0227,
            "modifiedValue" : 42230
    }
    
    else: abort(404)
    
    return jsonify({
        "inflation" : inflation,
        "pastyears" : pastyears
    })


def _is_valid_date(date_string):
    '''
    Helper function to check if a date string is valid
    
    Params:
        date_string (str): date string to check
    
    Returns:
        bool: True if valid, False if invalid
    '''
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False
