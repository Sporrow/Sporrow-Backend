from calendar import monthrange
from datetime import datetime
import re

from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.models.account import AccountModel
from app.models.interest import MinorInterestModel, MajorInterestModel
from app.models.sporrow import SporrowModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/sporrow/<id>/response')
class SporrowResponse(BaseResource):
    def post(self, id):
        """
        대여 제안 수락
        """

    def delete(self, id):
        """
        대여 제안 거절
        """