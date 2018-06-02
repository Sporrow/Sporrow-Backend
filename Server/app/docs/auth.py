from app.docs import SAMPLE_ACCESS_TOKEN, SAMPLE_REFRESH_TOKEN

CHECK_EMAIL_IS_CERTIFIED_GET = {
    'tags': ['로그인'],
    'description': '해당 이메일이 인증된 이메일인지 체크합니다',
    'parameters': [
        {
            'name': 'email',
            'description': '체크할 이메일',
            'in': 'path',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '인증된 이메일 입니다'
        },
        '204': {
            'description': '인증되지 않은 이메일 입니다'
        }
    }
}

AUTH_POST = {
    'tags': ['로그인'],
    'description': '유저 로그인',
    'parameters': [
        {
            'name': 'email',
            'description': '유저 이메일',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'pw',
            'description': '유저 비밀 번호',
            'in': 'json',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '로그인 성공',
            'examples': {
                '': {
                    'accessToken': SAMPLE_ACCESS_TOKEN,
                    'refreshToken': SAMPLE_REFRESH_TOKEN
                }
            }
        },
        '204': {
            'description': '인증되지 않은 이메일'
        },
        '205': {
            'description': '필수 정보가 입력되지 않음'
        },
        '401': {
            'description': '로그인 실패'
        }
    }
}

REFRESH_GET = {
    'tags': ['로그인'],
    'description': '토큰을 재발급합니다',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'Refresh Token',
            'in': 'header',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '토큰 재발급 성공',
            'examples': {
                '': {
                    'accessToken': SAMPLE_ACCESS_TOKEN
                }
            }
        },
        '205': {
            'description': '재로그인 필요'
        },
        '401': {
            'description': '토큰 인증 실패'
        }
    }
}
