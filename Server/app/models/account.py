from uuid import uuid4

from mongoengine import *

from app.models.interest import MajorInterestModel, MinorInterestModel


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    email = StringField(
        primary_key=True
    )

    email_certified = BooleanField(
        default=False
    )

    pw = StringField(
        required=True
    )

    nickname = StringField()

    major_category_interests = ListField(
        ReferenceField(
            document_type=MajorInterestModel,
            required=True
        )
    )

    minor_category_interests = ListField(
        ReferenceField(
            document_type=MinorInterestModel,
            required=True
        )
    )


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type=AccountModel,
        primary_key=True,
        reverse_delete_rule=CASCADE
    )

    identity = UUIDField(
        required=True,
        unique=True
    )

    @classmethod
    def generate_token(cls, model, owner):
        while True:
            uuid = uuid4()

            if not model.objects(identity=uuid):
                params = {
                    'owner': owner,
                    'identity': uuid
                }

                if isinstance(model, RefreshTokenModel):
                    params['pw_snapshot'] = owner.pw

                model(**params).save()

                return str(uuid)


class AccessTokenModel(TokenModel):
    meta = {
        'collection': 'token_access'
    }


class RefreshTokenModel(TokenModel):
    meta = {
        'collection': 'token_refresh'
    }

    pw_snapshot = StringField(
        required=True
    )
