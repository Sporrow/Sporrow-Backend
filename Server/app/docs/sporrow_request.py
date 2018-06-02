from app.docs import SAMPLE_OBJECT_IDS

SPORROW_REQUEST_LIST_GET={
    'tags': ['제안'],
    'description': '자신이 올린 모든 대여에 대한 제안 상태 조회',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '모든 대여에 대한 상태를 반환해줌',
            'examples': {
                '': {
                    'id': SAMPLE_OBJECT_IDS[3],
                    'requestCount': 5
                }
            }
        }
    }
}
SPORROW_REQUEST_POST={
    'tags': ['제안'],
    'description': '대여 신청',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        },
        {
            'name': 'borrowStartDate',
            'description': '대여 시작 날짜',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'borrowEndDate',
            'description': '대여 종료 날짜',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'tradeArea',
            'description': '대여 장소',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'tradeDate',
            'description': '대여 날짜',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'tradeTime',
            'description': '대여 시간',
            'in': 'json',
            'required': True
        }
    ],
    'responses': {
        '201': {
          'description': '제안 성공'
        },
        '204': {
            'description': '페이지 id 오류'
        },
        '400': {
            'description': '제안 실패'
        }
    }
}
SPORROW_REQUEST_GET= {
    'tags': ['제안'],
    'description': '특정 대여의 제안 상태(제안자 목록) 조회',
    'parameters':[
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        },
        {
            'name': 'id',
            'description': '페이지 id',
            'in': 'path',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '조회의 성공하고 목록을 반환함',
            'examples': {
                '': {
                    'id': SAMPLE_OBJECT_IDS[2],
                    'nickname': '조민귱',
                    'borrowStartDate': '2018-06-03',
                    'borrowEndDate': '2018-06-08'
                }
            }
        },
        '204': {
            'description': '페이지 id 오류'
        },
        '403': {
            'descrption': '조회한 사람과 대여 등록한 사람이 다름'
        }
    }
}
SPORROW_REQUEST_DETAIL_GET= {
    'tags':['제안'],
    'description': '특정 대여 신청의 세부 정보 조회',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        },
        {
            'name': 'id',
            'description': '페이지 id',
            'in': 'path',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '조회의 성공하고 정보를 반환합니다',
            'examples': {
                '': {
                    'borrowStateDate': '2018-06-03',
                    'borrowEndDate': '2018-06-04',
                    'tradeDate': '2018-06-02',
                    'tradeTime': '18:15:12',
                    'tradeArea': '대전'
                }
            }
        },
        '204': {
            'description': '페이지 id 오류',
        },
        '403': {
            'description': '대여 등록자와 조회자가 다름'
        }
    }
}