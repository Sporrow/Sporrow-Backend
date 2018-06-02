import re

from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.models.account import AccountModel
from app.models.sporrow import SporrowModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/sporrow')
class SporrowList(BaseResource):
    def __init__(self):
        self.sort_type_args_mapping = {
            '1': '-creation_time', # 최신순
            '2': '-cart_count', # 인기순
            '3': 'borrow_price_per_day', # 낮은 가격순
            '4': '-borrow_price_per_day' # 높은 가격순
        }

        self.pagination_count = 8

        super(SporrowList, self).__init__()

    @auth_required(AccountModel)
    def get(self):
        """
        스포츠용품 대여 리스트 조회
        """
        sort_type = request.args['sortType']
        page = request.args['page']

        if not re.match('\d+', page):
            abort(400)

        page = int(page)

        return [{
            'id': str(sporrow.id),
            'title': sporrow.title,
            'borrowPrice': sporrow.borrow_price_per_day,
            'includeWeekend': sporrow.include_weekend_on_price_calculation,
            'tradeArea': sporrow.trade_area
        } for sporrow in SporrowModel.objects.order_by(self.sort_type_args_mapping[sort_type])[(page - 1) * self.pagination_count:page * self.pagination_count]]

