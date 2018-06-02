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

    borrow_price_per_day = IntField(
        required=True
    )

    include_weekend_on_price_calculation = BooleanField(
        required=True
    )

    trade_start_time_hour = IntField(
        required=True
    )

    trade_end_time_hour = IntField(
        required=True
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
