from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from redis import Redis
from influxdb import InfluxDBClient

from mongoengine import connect

from app.views import Router


def create_app(*config_cls):
    """
    Creates Flask instance & initialize

    Returns:
        Flask
    """
    print('[INFO] Flask application initialized with {}'.format([config.__name__ for config in config_cls]))

    app_ = Flask(__name__)

    for config in config_cls:
        app_.config.from_object(config)

    CORS().init_app(app_)
    JWTManager().init_app(app_)
    Swagger(template=app_.config['SWAGGER_TEMPLATE']).init_app(app_)
    Router().init_app(app_)

    connect(**app_.config['MONGODB_SETTINGS'])
    app_.config['REDIS_CLIENT'] = Redis(**app_.config['REDIS_SETTINGS'])
    app_.config['INFLUXDB_CLIENT'] = InfluxDBClient(**app_.config['INFLUXDB_SETTINGS'])

    cfg = app_.config

    if cfg['INFLUXDB_SETTINGS']['database'] not in cfg['INFLUXDB_CLIENT'].get_list_database():
        cfg['INFLUXDB_CLIENT'].create_database(cfg['INFLUXDB_SETTINGS']['database'])

    app_.config['MAIL_CLIENT'] = Mail(app_)

    return app_
