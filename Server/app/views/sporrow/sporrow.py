from calendar import monthrange
from datetime import datetime

import re

from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.docs.sporrow import *
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
    @swag_from(SPORROW_CONTENT_GET)
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
            'cartCount': len(sporrow.in_cart),
            'inMyCart': g.user in sporrow.in_cart
        } for sporrow in SporrowModel.objects.order_by(self.sort_type_args_mapping[sort_type])[(page - 1) * self.pagination_count:page * self.pagination_count]])

    @auth_required(AccountModel)
    @json_required({'title': str, 'pictures': list, 'borrowPrice': int, 'includeWeekend': bool,
                    'minBorrowDays': int, 'maxBorrowDays': int, 'tradeStartHour': int, 'tradeEndHour': int,
                    'tradeArea': str, 'tradeAreaX': float, 'tradeAreaY': float, 'categories': list})
    @swag_from(SPORROW_LIST_POST)
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


@api.resource('/sporrow/<id>')
class SporrowContent(BaseResource):
    @swag_from(SPORROW_CONTENT_GET)
    def get(self, id):
        """
        스포츠용품 대여의 세부 정보 조회
        """
        if len(id) != 24:
            return Response('', 204)

        sporrow = SporrowModel.objects(id=id).first()

        if not sporrow:
            return Response('', 204)

        return self.unicode_safe_json_dumps({
            'title': sporrow.title,
            'owner': sporrow.owner.nickname,
            'cartCount': len(sporrow.in_cart),
            'inMyCart': g.user in sporrow.in_cart,
            'borrowPrice': sporrow.borrow_price_per_day,
            'tradeStartHour': sporrow.trade_start_hour,
            'tradeEndHour': sporrow.trade_end_hour,
            'tradeArea': sporrow.trade_area,
            'includeWeekend': sporrow.include_weekend_on_price_calculation
        })


@api.resource('/sporrow/<id>/calendar/<int:year>/<int:month>')
class SporrowCalendar(BaseResource):
    def __init__(self):
        self.date_format = '{}-{:0>2}-{:0>2}'

        super(SporrowCalendar, self).__init__()

    @auth_required(AccountModel)
    @swag_from(SPORROW_CALENDAR_GET)
    def get(self, id, year, month):
        """
        스포츠용품 대여의 달력 조회
        """
        if len(id) != 24:
            return Response('', 204)

        sporrow = SporrowModel.objects(id=id).first()

        if not sporrow:
            return Response('', 204)

        if year < datetime.now().year or\
                (year == datetime.now().year and month < datetime.now().month):
            abort(400)

        last_day_of_month = monthrange(year, month)[1]

        return { day: 1 if self.date_format.format(year, month, day) not in sporrow.borrow_calendar else 0 for day in range(1, last_day_of_month + 1) }
        # 1 : 대여 가능한 날
        # 0 : 대여 불가능한 날
