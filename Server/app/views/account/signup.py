from string import ascii_uppercase, digits
import random

from flask import Blueprint, Response, abort, current_app, request
from flask_mail import Mail, Message
from flask_restful import Api
from flasgger import swag_from

from redis import Redis

from werkzeug.security import generate_password_hash

from app.docs.signup import *
from app.models.account import AccountModel
from app.models.interest import MajorInterestModel, MinorInterestModel
from app.views import BaseResource, json_required

api = Api(Blueprint(__name__, __name__))


def generate_email_certification_code(email):
    redis_client = current_app.config['REDIS_CLIENT']

    while True:
        code = ''.join(random.choice(ascii_uppercase + digits) for _ in range(12))

        if not redis_client.exists(code):
            redis_client.set(code, email, ex=60 * 5)

            return code


@api.resource('/check/<email>')
class IDDuplicationCheck(BaseResource):
    @swag_from(ID_DUPLICATION_CHECK_GET)
    def get(self, email):
        """
        이메일 중복체크
        """
        if AccountModel.objects(email=email):
            abort(409)
        else:
            return Response('', 200)


@api.resource('/signup')
class Signup(BaseResource):
    @swag_from(SIGNUP_POST)
    @json_required({'email': str, 'pw': str})
    def post(self):
        """
        회원가입
        """
        payload = request.json

        email = payload['email']
        pw = payload['pw']

        if AccountModel.objects(email=email):
            return Response('', 409)

        mail_client = current_app.config['MAIL_CLIENT']

        code = generate_email_certification_code(email)

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


@api.resource('/email-resend/<email>')
class EmailResend(BaseResource):
    @swag_from(EMAIL_RESEND_GET)
    def get(self, email):
        """
        이메일 재전송
        """
        if not AccountModel.objects(email=email):
            return Response('', 204)

        mail_client = current_app.config['MAIL_CLIENT']

        code = generate_email_certification_code(email)

        msg = Message('Please verify user email', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
        msg.html = '<a href="http://{0}:{1}/certify/{2}">인증하기</a>'.format(
            current_app.config['REPRESENTATIVE_HOST'] or current_app.config['HOST'],
            current_app.config['PORT'] if not current_app.testing else 80,
            code
        )

        mail_client.send(msg)

        return Response('', 200)


@api.resource('/info/initialize/<email>')
class InitializeInfo(BaseResource):
    @swag_from(INITIALIZE_INFO_POST)
    @json_required({'nickname': str, 'categories': list})
    def post(self, email):
        """
        기본 정보 업로드(초기화)
        """
        payload = request.json

        nickname = payload['nickname']
        categories = payload['categories']

        user = AccountModel.objects(email=email).first()

        if not user.email_certified:
            abort(401)

        if not user:
            return Response('', 204)

        if AccountModel.objects(nickname=nickname):
            abort(409)

        user.nickname = nickname

        for category_id in categories:
            major_interest = MajorInterestModel.objects(id=category_id).first()
            minor_interest = MinorInterestModel.objects(id=category_id).first()

            if major_interest:
                user.major_interests.append(major_interest)
            elif minor_interest:
                user.minor_interests.append(minor_interest)
            else:
                abort(400)

        user.save()

        return Response('', 201)


@api.resource('/certify/<code>')
class EmailCertify(BaseResource):
    def get(self, code):
        """
        이메일 인증 URL
        """
        redis_client = current_app.config['REDIS_CLIENT']

        email = redis_client.get(code)

        if not email:
            abort(401)

        user = AccountModel.objects(email=email).first()

        if not user:
            abort(401)

        user.update(email_certified=True)

        redis_client.delete(code)

        return Response('Welcome!', 201)
