from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('configs.ProdConfig')
    
    CORS(app)

    db.init_app(app)
    
    from .routes.alerts import alertview
    from .routes.climate_controls import climateview
    from .routes.util_view import utilities
    from .routes.weather import weathterWidget
    from .routes.rooms import devices
    from .routes.sensor_updates import sensor_updates
    from .routes.inflation_calc import inflation_calc

    app.register_blueprint(weathterWidget, url_prefix='/')
    app.register_blueprint(devices, url_prefix="/")
    app.register_blueprint(alertview, url_prefix='/')
    app.register_blueprint(climateview, url_prefix='/')
    app.register_blueprint(utilities, url_prefix='/')
    app.register_blueprint(sensor_updates, url_prefix='/')
    app.register_blueprint(inflation_calc, url_prefix='/')

    from .DatabaseModels import Sensors, Activity, AC_Activity

    with app.app_context():
        db.create_all()
        print("context created")

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app



