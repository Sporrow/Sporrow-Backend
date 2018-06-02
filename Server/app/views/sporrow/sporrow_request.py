from datetime import datetime

from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.docs.sporrow_request import *
from app.models.account import AccountModel
from app.models.sporrow import SporrowModel, SporrowRequestModel
from app.views import BaseResource, auth_required, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/sporrow/request')
class SporrowRequestList(BaseResource):
    @auth_required(AccountModel)
    @swag_from(SPORROW_REQUEST_LIST_GET)
    def get(self):
        """
        자신이 올린 모든 대여에 대한 제안 상태 조회
        """
        return self.unicode_safe_json_dumps([{
            'id': str(sporrow.id),
            'requestCount': SporrowRequestModel.objects(sporrow=sporrow).count()
        } for sporrow in SporrowModel.objects(owner=g.user)])


@api.resource('/sporrow/request/<id>')
class SporrowRequest(BaseResource):
    @auth_required(AccountModel)
    @json_required({'borrowStartDate': str, 'borrowEndDate': str, 'tradeArea': str, 'tradeDate': str, 'tradeTime': str})
    @swag_from(SPORROW_REQUEST_POST)
    def post(self, id):
        """
        대여 제안
        """
        if len(id) != 24:
            return Response('', 204)

        sporrow = SporrowModel.objects(id=id).first()

        if not sporrow:
            return Response('', 204)

        payload = request.json

        borrow_start_date = payload['borrowStartDate']
        borrow_end_date = payload['borrowEndDate']
        trade_area = payload['tradeArea']
        trade_date = payload['tradeDate']
        trade_time = payload['tradeTime']

        if datetime.strptime(borrow_end_date, '%Y-%m-%d') - datetime.strptime(borrow_start_date, '%Y-%m-%d') < sporrow.min_borrow_days - 1 or\
                datetime.strptime(trade_date, '%Y-%m-%d') > datetime.strptime(borrow_start_date, '%Y-%m-%d') or \
                not sporrow.trade_start_hour <= datetime.strptime(trade_time, '%H:%M').time().hour <= sporrow.trade_end_hour:
            abort(400)

        SporrowRequestModel(
            requester=g.user,
            sporrow=sporrow,
            borrow_start_date=borrow_start_date,
            borrow_end_date=borrow_end_date,
            trade_area=trade_area,
            trade_date=trade_date,
            trade_time=trade_time
        ).save()

        return Response('', 201)

    @auth_required(AccountModel)
    @swag_from(SPORROW_REQUEST_GET)
    def get(self, id):
        """
        특정 대여의 제안 상태(제안자 목록)조회
        """
        if len(id) != 24:
            return Response('', 204)

        sporrow = SporrowModel.objects(id=id).first()

        if not sporrow:
            return Response('', 204)

        if sporrow.owner != g.user:
            abort(403)

        return self.unicode_safe_json_dumps([{
            'id': str(req.id),
            'nickname': req.requester.nickname,
            'borrowStartDate': req.borrow_start_date,
            'borrowEndDate': req.borrow_end_date
        } for req in SporrowRequestModel.objects(sporrow=sporrow)])


@api.resource('/sporrow/request/detail/<id>')
class SporrowRequestDetail(BaseResource):
    @auth_required(AccountModel)
    def get(self, id):
        """
        특정 제안의 세부 정보 조회
        """
        if len(id) != 24:
            return Response('', 204)

        req = SporrowRequestModel.objects(id=id).first()

        if not req:
            return Response('', 204)

        if req.sporrow.owner != g.owner:
            abort(403)

        return self.unicode_safe_json_dumps({
            'borrowStartDate': req.borrow_start_date,
            'borrowEndDate': req.borrow_end_date,
            'tradeDate': req.trade_date,
            'tradeTime': req.trade_time,
            'tradeArea': req.area
        })
