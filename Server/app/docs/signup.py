from app.docs import SAMPLE_OBJECT_IDS

ID_DUPLICATION_CHECK_GET = {
    'tags': ['회원가입'],
    'description': '이메일이 이미 가입되었는지를 체크(중복체크)합니다.',
    'parameters': [
        {
            'name': 'email',
            'description': '중복을 체크할 이메일',
            'in': 'path',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '중복되지 않음',
        },
        '409': {
            'description': '중복됨'
        }
    }
}

SIGNUP_POST = {
    'tags': ['회원가입'],
    'description': '회원가입합니다.',
    'parameters': [
        {
            'name': 'email',
            'description': '이메일',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'pw',
            'description': '비밀번호',
            'in': 'json',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '회원가입 성공, 인증 이메일 발송 완료. 기본 정보 초기화 액티비티로 이동하면 됩니다. 인증 이메일의 유효 시간은 5분입니다.',
        },
        '409': {
            'description': '이메일 중복됨'
        }
    }
}

EMAIL_RESEND_GET = {
    'tags': ['회원가입'],
    'description': '인증 메일을 재전송합니다.',
    'parameters': [
        {
            'name': 'email',
            'description': '인증 메일을 재전송할 이메일',
            'in': 'path',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '이메일 재전송 성공',
        },
        '204': {
            'description': '가입되지 않은 이메일'
        }
    }
}

INITIALIZE_INFO_POST = {
    'tags': ['회원가입'],
    'description': '기본 정보를 업로드합니다.',
    'parameters': [
        {
            'name': 'email',
            'description': '기본 정보 업로드 대상 이메일',
            'in': 'path',
            'type': 'str',
            'required': True
        },
        {
            'name': 'nickname',
            'description': '닉네임',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'categories',
            'description': '관심사 ID 목록 ex) ["{}"], ["{}"], ["{}"]'.format(*SAMPLE_OBJECT_IDS),
            'in': 'json',
            'type': 'list',
            'required': True
        }
    ],
    'responses': {
        '201': {
            'description': '업로드 성공',
        },
        '204': {
            'description': '가입되지 않은 이메일'
        },
        '400': {
            'description': '관심사 ID 중 존재하지 않는 관심사가 존재함'
        },
        '401': {
            'description': '이메일 인증되지 않음'
        },
        '409': {
            'description': '닉네임이 중복됨'
        }
    }
}
