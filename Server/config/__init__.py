from datetime import timedelta
import os


class Config:
    SERVICE_NAME = 'Sporrow'
    SERVICE_NAME_UPPER = SERVICE_NAME.upper()
    REPRESENTATIVE_HOST = None

    RUN_SETTING = {
        'threaded': True
    }

    SECRET_KEY = os.getenv('SECRET_KEY', '85c145a16bd6f6e1f3e104ca78c6a102')
    # Secret key for any 3-rd party libraries

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=365)
    JWT_HEADER_TYPE = 'JWT'

    MAIL_SERVER, MAIL_PORT = 'smtp.gmail.com', 587
    MAIL_USERNAME, MAIL_PASSWORD, MAIL_USE_TLS = 'sporrow33', 'uursty199', True

    MONGODB_SETTINGS = {
        'host': None,
        'port': None,
        'username': None,
        'password': os.getenv('MONGO_PW_{}'.format(SERVICE_NAME_UPPER)),
        'db': SERVICE_NAME
    }

    REDIS_SETTINGS = {
        'host': 'localhost',
        'port': 6379,
        'password': os.getenv('REDIS_PW_{}'.format(SERVICE_NAME_UPPER)),
        'db': 0
    }

    INFLUXDB_SETTINGS = {
        'host': 'localhost',
        'port': 8086,
        'username': 'root',
        'password': os.getenv('INFLUX_PW_{}'.format(SERVICE_NAME_UPPER), 'root'),
        'database': SERVICE_NAME.replace('-', '_')
    }

    SWAGGER = {
        'title': SERVICE_NAME,
        'specs_route': os.getenv('SWAGGER_URI', '/docs'),
        'uiversion': 3,

        'info': {
            'title': SERVICE_NAME + ' API',
            'version': '1.0',
            'description': ''
        },
        'basePath': '/ '
    }

    SWAGGER_TEMPLATE = {
        'schemes': [
            'http'
        ],
        'tags': [
            {
                'name': '로그인',
                'description': '로그인 관련 API'
            },
            {
                'name': '회원가입',
                'description': '회원가입 관련 API'
            }
        ]
    }
