from mongoengine import *


class InterestBase(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    name = StringField(
        required=True
    )


class MajorInterestModel(InterestBase):
    meta = {
        'interest_major'
    }


class MinorInterestModel(InterestBase):
    meta = {
        'interest_minor'
    }

    parent_interest = ReferenceField(
        document_type=MajorInterestModel,
        required=True
    )
