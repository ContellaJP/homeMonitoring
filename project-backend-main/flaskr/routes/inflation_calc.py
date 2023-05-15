from flask import Blueprint, request, jsonify, abort
from .. import db
from ..DatabaseModels import Activity
from datetime import date
from sqlalchemy import func



inflation_calc = Blueprint('inflation', __name__)

@inflation_calc.route('/inflation-calculator/', methods=['GET','POST'])

def inflation_calculator():
    """
    Calculates the estimated monthly and yearly costs for power and water, inflates them by the given percentages, and returns the results

    GET method:
    - Returns the estimated costs for the current date, inflated by 0.6% and 6.5% for monthly and yearly costs


    Returns:
    - A JSON object containing the following keys:
      * "totalMonth": The total monthly cost, inflated by 0.6%. (0.6% is the average rate of change for inflation from month to month in 2022)
      * "totalYear": The total yearly cost, inflated by 6.5%. (USIR 2022 was 6.5%)
    """
    if request.method == "GET":
        queryPowerSum = db.session.query(func.sum(Activity.power_price)).filter_by(start_date=date.today())
        queryWaterSum = db.session.query(func.sum(Activity.water_price)).filter_by(start_date=date.today())

        if queryPowerSum is None:
            abort(404)

        if queryWaterSum is None:
            abort(404)
        
        for i in queryPowerSum.first():
            estimatePowerCost = i + 30.437 #30.437 = AVG DAYS IN A MONTH

        for i in queryWaterSum.first():
            estimateWaterCost = i + 30.437

        totalCost = estimatePowerCost + estimateWaterCost

        inflatedCostMonthly = totalCost * (1 + .6 / 100)

        inflatedCostYearly = (totalCost * 12) * (1 + 6.5 / 100)

    return jsonify ({"totalInflatedMonth": inflatedCostMonthly, "totalInflatedYear": inflatedCostYearly})
        