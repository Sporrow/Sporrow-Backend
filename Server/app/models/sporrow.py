from datetime import datetime

from mongoengine import *

from app.models.account import AccountModel
from app.models.interest import MajorInterestModel, MinorInterestModel


class SporrowModel(Document):
    meta = {
        'collection': 'sporrow'
    }

    creation_time = DateTimeField(
        default=datetime
    )
    # 대여 업로드 시간

    owner = ReferenceField(
        document_type=AccountModel,
        required=True
    )
    # 주인

    title = StringField(
        required=True
    )
    # 제목

    pictures = ListField()
    # 사진 목록. base64 인코딩된 문자열

    borrow_price_per_day = IntField(
        required=True,
        min_value=0
    )
    # 대여비 / 일

    include_weekend_on_price_calculation = BooleanField(
        required=True
    )
    # 주말 대여를 대여비 계산에 포함시킬지

    min_borrow_days = IntField(
        required=True,
        min_value=1
    )
    # 최소 대여일

    max_borrow_days = IntField(
        required=True,
        min_value=1
    )
    # 최대 대여일

    trade_start_hour = IntField(
        required=True,
        min_value=0,
        max_value=24
    )
    # 거래 가능 시간 : 시작

    trade_end_hour = IntField(
        required=True,
        min_value=0,
        max_value=24
    )
    # 거래 가능 시간 : 종료

    trade_area = StringField(
        required=True
    )
    # 거래 장소

    trade_area_x = FloatField(
        required=True
    )
    # 거래 장소 X position
    
    trade_area_y = FloatField(
        required=True
    )
    # 거래 장소 Y position

    major_interests = ListField(
        ReferenceField(
            document_type=MajorInterestModel,
            required=True
        )
    )
    # 1차 카테고리

    minor_interests = ListField(
        ReferenceField(
            document_type=MinorInterestModel,
            required=True
        )
    )
    # 2차 카테고리

    in_cart = ListField(
        ReferenceField(
            document_type=AccountModel,
            required=True
        )
    )
    # 이 대여를 카트에 담은 사람
    # 여기선 count만 하고 AccountModel에 cart 필드를 두는 게 좋을 거 같음

    borrow_calendar = DictField()
    # 대여 가능/불가능을 flagging하기 위한 달력 표기용 필드


class SporrowRequestModel(Document):
    meta = {
        'collection': 'sporrow_request'
    }

    requester = ReferenceField(
        document_type=AccountModel,
        required=True
    )
    # 대여 제안자

    sporrow = ReferenceField(
        document_type=SporrowModel,
        required=True
    )
    # 대여

    borrow_start_date = StringField(
        required=True
    )
    # 대여 시작일

    borrow_end_date = StringField(
        required=True
    )
    # 대여 종료일

    trade_area = StringField(
        required=True
    )
    # 희망 거래 장소

    trade_date = StringField(
        required=True
    )
    # 희망 거래일

    trade_time = StringField(
        required=True
    )
    # 희망 거래 시간
