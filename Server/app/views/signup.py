from string import ascii_uppercase, digits
import random

from flask import Blueprint, Response, abort, current_app, request
from flask_mail import Mail, Message
from flask_restful import Api

from redis import Redis

from werkzeug.security import generate_password_hash

from app.models.account import AccountModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))


@api.resource('/check/<email>')
class IDDuplicationCheck(BaseResource):
    def get(self, email):
        if AccountModel.objects(email=email):
            abort(409)
        else:
            return Response('', 200)


@api.resource('/signup')
class Signup(BaseResource):
    @json_required({'email': str, 'pw': str})
    def post(self):
        def generate_email_certification_code():
            while True:
                code = ''.join(random.choice(ascii_uppercase + digits) for _ in range(12))

                if not redis_client.exists(code):
                    redis_client.set(code, email, ex=60 * 5)

                    return code

        payload = request.json

        email = payload['email']
        pw = payload['pw']

        if AccountModel.objects(email=email):
            return Response('', 204)

        redis_client: Redis = current_app.config['REDIS_CLIENT']
        mail_client: Mail = current_app.config['MAIL_CLIENT']

        code = generate_email_certification_code()

        msg = Message('Please verify user email', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.html = '<a href="http://{0}:{1}/certify/{2}">인증하기</a>'.format(
            current_app.config['REPRESENTATIVE_HOST'] or current_app.config['HOST'],
            current_app.config['PORT'] if not current_app.testing else 80,
            code
        )

        mail_client.send(msg)

        AccountModel(
            email=email,
            pw=generate_password_hash(pw)
        ).save()

        return Response('', 201)


@api.resource('/certify/<code>')
class EmailCertify(BaseResource):
    def get(self, code):
        """
        이메일 인증 URL
        """
        redis_client: Redis = current_app.config['REDIS_CLIENT']

        email = redis_client.get(code)

        if not email:
            abort(401)

        user = AccountModel.objects(email=email).first()

        if not user:
            abort(401)

        user.update(email_certified=True)

        redis_client.delete(code)

        return Response('Welcome!', 201)
