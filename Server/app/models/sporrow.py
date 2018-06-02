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

    owner = ReferenceField(
        document_type=AccountModel,
        required=True
    )

    title = StringField(
        required=True
    )

    pictures = ListField()

    borrow_price_per_day = IntField(
        required=True,
        min_value=0
    )

    include_weekend_on_price_calculation = BooleanField(
        required=True
    )

    min_borrow_days = IntField(
        required=True,
        min_value=1
    )

    max_borrow_days = IntField(
        required=True,
        min_value=1
    )

    trade_start_hour = IntField(
        required=True,
        min_value=0,
        max_value=24
    )

    trade_end_hour = IntField(
        required=True,
        min_value=0,
        max_value=24
    )

    trade_area = StringField(
        required=True
    )

    trade_area_x = FloatField(
        required=True
    )
    
    trade_area_y = FloatField(
        required=True
    )

    major_interests = ListField(
        ReferenceField(
            document_type=MajorInterestModel,
            required=True
        )
    )

    minor_interests = ListField(
        ReferenceField(
            document_type=MinorInterestModel,
            required=True
        )
    )

    in_cart = ListField(
        ReferenceField(
            document_type=AccountModel,
            required=True
        )
    )
