from string import ascii_uppercase, digits
import random

from flask import Blueprint, Response, abort, current_app, request
from flask_mail import Mail, Message
from flask_restful import Api

from redis import Redis

from werkzeug.security import generate_password_hash

from app.models.account import AccountModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/check/<email>')
class IDDuplicationCheck(BaseResource):
    def get(self, email):
        if AccountModel.objects(email=email):
            abort(409)
        else:
            return Response('', 200)

