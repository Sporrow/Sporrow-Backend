from uuid import uuid4

from mongoengine import *


class AccountModel(Document):
    meta = {
        'collection': 'account'
    }

    id = StringField(
        primary_key=True
    )

    pw = StringField(
        required=True
    )


class TokenModel(Document):
    meta = {
        'abstract': True,
        'allow_inheritance': True
    }

    owner = ReferenceField(
        document_type='AccountModel',
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
        'collection': 'access_token'
    }


class RefreshTokenModel(TokenModel):
    meta = {
        'collection': 'refresh_token'
    }

    pw_snapshot = StringField(
        required=True
    )