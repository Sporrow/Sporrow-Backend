import random
import re

from flask import Blueprint, abort, request
from flask_restful import Api

from app.models.interest import MajorInterestModel, MinorInterestModel
from app.views import BaseResource

api = Api(Blueprint(__name__, __name__))


@api.resource('/interest-list')
class InterestList(BaseResource):
    def get(self):
        """
        관심사(스포츠 관련 카테고리) 리스트 반환
        """
        size = request.args['size']

        if not re.match('\d+', size):
            abort(400)

        size = int(size)

        major_interest_count = size // 3
        minor_interest_count = size - major_interest_count

        return self.unicode_safe_json_dumps([{
            'id': str(interest.id),
            'name': interest.name
        } for interest in random.shuffle(MajorInterestModel.objects[:major_interest_count] + MinorInterestModel.objects[:minor_interest_count])])


@api.resource('/interest-list/<keyword>')
class InterestListSearch(BaseResource):
    def get(self, keyword):
        """
        관심사 리스트 검색
        """
        if not keyword:
            abort(400)

        regex = re.compile('.*{}.*'.format(keyword))

        return self.unicode_safe_json_dumps([{
            'id': str(interest.id),
            'name': interest.name
        } for interest in random.shuffle(MajorInterestModel.objects(name=regex) + MinorInterestModel.objects(name=regex))])
