from flask import Blueprint, jsonify
import requests

weathterWidget = Blueprint('weathterWidget', __name__)

@weathterWidget.route('/weatherWidgetData', methods=["GET"])
def weatherWidgetdata():
    '''
    provides the needed data for the weather widget. 

    Method: GET
    
    return:
        (JSON) 
        {
            "current-temp" : (int) current temperature,
            "high" : (int) high temperature,
            "low" : (int) low temperature,
            "condition" : (string) weather condition, WMO weather code provided below,
        }

    WMO Weather interpretation codes
    Code	    Description
    0	        Clear sky
    1, 2, 3 	Mainly clear, partly cloudy, and overcast
    45, 48	    Fog and depositing rime fog
    51, 53, 55	Drizzle: Light, moderate, and dense intensity
    56, 57	    Freezing Drizzle: Light and dense intensity
    61, 63, 65	Rain: Slight, moderate and heavy intensity
    66, 67	    Freezing Rain: Light and heavy intensity
    71, 73, 75	Snow fall: Slight, moderate, and heavy intensity
    77	        Snow grains
    80, 81, 82	Rain showers: Slight, moderate, and violent
    85, 86	    Snow showers slight and heavy
    95 *	    Thunderstorm: Slight or moderate
    96, 99 *	Thunderstorm with slight and heavy hail

    (*) Thunderstorm forecast with hail is only available in Central Europe
    '''
    weather = _getWeather()
    curr_temp = weather["current_weather"]["temperature"]
    high = weather["daily"]["temperature_2m_max"][0]
    low = weather["daily"]["temperature_2m_min"][0]
    weather_code = weather["current_weather"]["weathercode"]

    return jsonify({
            "current-temp" : curr_temp,
            "high" : high,
            "low" : low,
            "condition": weather_code
        }), 200

def _getWeather():
    '''
    helper method to get the weather data from the open-meteo API
    '''
    url = "https://api.open-meteo.com/v1/forecast?latitude=33.50&longitude=-86.81&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch&timezone=America/Chicago&forecast_days=1&current_weather=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return ("Error:", response.status_code)