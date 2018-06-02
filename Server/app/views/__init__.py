from functools import wraps
from uuid import UUID
import gzip
import time

import ujson

from flask import Response, abort, after_this_request, current_app, g, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.exceptions import HTTPException

from app.models.account import AccessTokenModel


def after_request(response):
    """
    Set header - X-Content-Type-Options=nosniff, X-Frame-Options=deny before response
    """
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'deny'

    current_app.config['INFLUXDB_CLIENT'].write_points([
        {
            'measurement': 'api_process_data',
            'tags': {
                'status': response.status,
                'method': request.method,
                'uri': request.path
            },
            'fields': {
                'count': 1
            }
        }
    ])

    return response


def exception_handler(e):
    print(e)

    if isinstance(e, HTTPException):
        description = e.description
        code = e.code
    elif isinstance(e, BaseResource.ValidationError):
        description = e.description
        code = 400
    else:
        description = ''
        code = 500

    return jsonify({
        'msg': description
    }), code


def gzipped(fn):
    """
    View decorator for gzip compress the response body
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        @after_this_request
        def zipper(response):
            if 'gzip' not in request.headers.get('Accept-Encoding', '')\
                    or not 200 <= response.status_code < 300\
                    or 'Content-Encoding' in response.headers:
                # 1. Accept-Encoding에 gzip이 포함되어 있지 않거나
                # 2. 200번대의 status code로 response하지 않거나
                # 3. response header에 이미 Content-Encoding이 명시되어 있는 경우
                return response

            response.data = gzip.compress(response.data)
            response.headers.update({
                'Content-Encoding': 'gzip',
                'Vary': 'Accept-Encoding',
                'Content-Length': len(response.data)
            })

            return response
        return fn(*args, **kwargs)
    return wrapper


def auth_required(model):
    def decorator(fn):
        """
        View decorator for access control
        """
        @wraps(fn)
        @jwt_required
        def wrapper(*args, **kwargs):
            token = AccessTokenModel.objects(identity=UUID(get_jwt_identity())).first()
            if not token or not isinstance(token.owner, model):
                abort(403)

            g.user = token.owner

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def json_required(required_keys):
    """
    View decorator for JSON validation.

    - If content-type is not application/json : returns status code 406
    - If required_keys are not exist on request.json : returns status code 400

    Args:
        required_keys (dict): Required keys on requested JSON payload
    """
    def decorator(fn):
        if fn.__name__ == 'get':
            print('[WARN] JSON with GET method? on "{}()"'.format(fn.__qualname__))

        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not request.is_json:
                abort(406)

            for key, typ in required_keys.items():
                if key not in request.json or not type(request.json[key]) is typ:
                    abort(400)
                if typ is str and not request.json[key]:
                    abort(400)

            return fn(*args, **kwargs)
        return wrapper
    return decorator


class BaseResource(Resource):
    """
    BaseResource with some helper functions based flask_restful.Resource
    """
    def __init__(self):
        self.now = time.strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def unicode_safe_json_dumps(cls, data, status_code=200, **kwargs) -> Response:
        """
        Helper function which processes json response with unicode using ujson

        Args:
            data (dict and list): Data for dump to JSON
            status_code (int): Status code for response
        """
        return Response(
            ujson.dumps(data, ensure_ascii=False),
            status_code,
            content_type='application/json; charset=utf8',
            **kwargs
        )

    class ValidationError(Exception):
        def __init__(self, description='', *args):
            self.description = description

            super(BaseResource.ValidationError, self).__init__(*args)


class Router:
    """
    REST resource routing helper class like standard flask 3-rd party libraries
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Routes resources. Use app.register_blueprint() aggressively
        """
        app.after_request(after_request)
        app.register_error_handler(Exception, exception_handler)

        from app.views.account import auth, signup
        from app.views.sporrow import sporrow,sporrow_request
        app.register_blueprint(auth.api.blueprint)
        app.register_blueprint(signup.api.blueprint)
        app.register_blueprint(sporrow.api.blueprint)
        app.register_blueprint(sporrow_request.api.blueprint)
