import re

from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.models.account import AccountModel
from app.models.interest import MinorInterestModel, MajorInterestModel
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

        return self.unicode_safe_json_dumps([{
            'id': str(sporrow.id),
            'title': sporrow.title,
            'borrowPrice': sporrow.borrow_price_per_day,
            'includeWeekend': sporrow.include_weekend_on_price_calculation,
            'tradeArea': sporrow.trade_area,
            'cartCount': len(sporrow.in_cart)
        } for sporrow in SporrowModel.objects.order_by(self.sort_type_args_mapping[sort_type])[(page - 1) * self.pagination_count:page * self.pagination_count]])

    @auth_required(AccountModel)
    @json_required({'title': str, 'pictures': list, 'borrowPrice': int, 'includeWeekend': bool,
                    'minBorrowDays': int, 'maxBorrowDays': int, 'tradeStartHour': int, 'tradeEndHour': int,
                    'tradeArea': str, 'tradeAreaX': float, 'tradeAreaY': float, 'categories': list})
    def post(self):
        """
        스포츠용품 업로드
        """
        payload = request.json

        title = payload['title']
        pictures = payload['pictures']
        borrow_price_per_day = payload['borrowPrice']
        include_weekend_on_price_calculation = payload['includeWeekend']
        min_borrow_days = payload['minBorrowDays']
        max_borrow_days = payload['maxBorrowDays']
        trade_start_hour = payload['tradeStartHour']
        trade_end_hour = payload['tradeEndHour']
        trade_area = payload['tradeArea']
        trade_area_x = payload['tradeAreaX']
        trade_area_y = payload['tradeAreaY']
        categories = payload['categories']

        if borrow_price_per_day < 0 or\
                min_borrow_days < 1 or\
                max_borrow_days < 1 or\
                max_borrow_days < min_borrow_days or\
                not 0 <= trade_start_hour <= 24 or\
                not 0 <= trade_end_hour <= 24 or\
                trade_end_hour < trade_start_hour:
            abort(400)

        sporrow = SporrowModel(
            owner=g.user,
            title=title,
            pictures=pictures,
            borrow_price_per_day=borrow_price_per_day,
            include_weekend_on_price_calculation=include_weekend_on_price_calculation,
            min_borrow_days=min_borrow_days,
            max_borrow_days=max_borrow_days,
            trade_start_hour=trade_start_hour,
            trade_end_hour=trade_end_hour,
            trade_area=trade_area,
            trade_area_x=trade_area_x,
            trade_area_y=trade_area_y
        )

        for category_id in categories:
            major_interest = MajorInterestModel.objects(id=category_id).first()
            minor_interest = MinorInterestModel.objects(id=category_id).first()

            if major_interest:
                sporrow.major_interests.append(major_interest)
            elif minor_interest:
                sporrow.minor_interests.append(minor_interest)
            else:
                abort(400)

        sporrow.save()

        return Response('', 201)

