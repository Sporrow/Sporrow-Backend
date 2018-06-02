from uuid import UUID

from flask import Blueprint, Response, abort, request
from flask_jwt_extended import get_jwt_identity, jwt_refresh_token_required
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Api

from app.models.account import AccountModel, TokenModel, AccessTokenModel, RefreshTokenModel
from app.views import BaseResource, json_required

from werkzeug.security import check_password_hash

api = Api(Blueprint(__name__, __name__))

@api.resource('/is-certified/<email>')
class CheakEmailIsCertified(BaseResource):
    def get(self,email):
        return Response('',200 if AccountModel.objects(email=email).first().email_certified else 204)


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

                elif not all((user.nickname, user.major_category_interests or user.minor_category_interests)):
                    return Response('', 205)

                return {
                    'accessToken': create_access_token(TokenModel.generate_token(AccessTokenModel, user)),
                    'refreshToken': create_refresh_token(TokenModel.generate_token(RefreshTokenModel, user))
                }
            else:
                abort(401)
        else:
            abort(401)


@api.resource('/refresh')
class Refresh(BaseResource):
    @jwt_refresh_token_required
    def get(self):
        refresh_token = RefreshTokenModel.objects(identity=UUID(get_jwt_identity())).first()

        if refresh_token:
            if refresh_token.pw_snapshot == refresh_token.owner.pw:
                return {
                    'accessToken': create_refresh_token(TokenModel.generate_token(AccessTokenModel, refresh_token.owner))
                }
            else:
                return Response('', 205)
        else:
            abort(401)
