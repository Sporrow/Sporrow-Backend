from uuid import UUID

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Api

from app.models.account import AccountModel, TokenModel, AccessTokenModel, RefreshTokenModel
from app.views import BaseResource, json_required

from werkzeug.security import check_password_hash

api = Api(Blueprint(__name__, __name__))


@api.resource('/auth')
class Auth(BaseResource):
    @json_required({'email': str, 'pw': str})
    def post(self):
        payload = request.json

        email = payload['email']
        pw = payload['pw']

        user = AccountModel.objects(email=email).first()

        if user:
            if check_password_hash(user.pw, pw):
                if not user.email_certified:
                    return Response('', 204)

                return {
                    'accessToken': create_access_token(TokenModel.generate_token(AccessTokenModel, user)),
                    'refreshToken': create_refresh_token(TokenModel.generate_token(RefreshTokenModel, user))
                }
            else:
                abort(401)
        else:
            abort(401)

