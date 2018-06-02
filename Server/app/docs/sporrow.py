from app.docs import SAMPLE_OBJECT_IDS

SPORROW_LIST_GET={
    'tags': ['대여'],
    'description': '등록된 리스트를 반환합니다',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        },
        {
            'name': 'sortType',
            'description': '정렬 모드',
            'in': 'path',
            'type': 'str',
            'required': True
        },
        {
            'name': 'page',
            'description': '페이지',
            'in': 'path',
            'type': 'int',
            'required': True
        }
    ],
    'responses': {
        '200': {
            'description': '조회에 성공했고 리스트를 반환합니다',
            'examples': {
                '': [
                     {
                        'id': SAMPLE_OBJECT_IDS[1],
                        'title': '조민규 운동화 빌려드려요',
                        'borrowPrice': 3000,
                        'includeWeekend': True,
                        'tradeArea': '대구',
                        'cartCount': 113,
                        'inMyCart': True
                     },
                     {
                        'id': SAMPLE_OBJECT_IDS[0],
                        'title': '조민규 축구화 빌려드려요',
                        'borrowPrice': 12000,
                        'includeWeekend': False,
                        'tradeArea': '대전',
                        'cartCount': 12341,
                        'inMyCart': False
                     },
                ]
            }
        },
        '400': {
            'description': '리스트 조회 실패'
        }
    }
}
SPORROW_LIST_POST={
    'tags': ['대여'],
    'description': '용품을 업로드합니다',
    'parameters': [
        {
            'name': 'Authorization',
            'description': 'JWT Token(JWT ***)',
            'in': 'header',
            'type': 'str',
            'required': True
        },
        {
            'name': 'title',
            'description': '제목',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'pictures',
            'description': '용품 이미지. 각 이미지는 base64로 인코딩된 문자열 입니다',
            'in': 'json',
            'type': 'list',
            'required': False
        },
        {
            'name': 'borrowPrice',
            'description': '하루당 대여비',
            'in': 'json',
            'type': 'int',
            'required':True
        },
        {
            'name': 'includeWeekend',
            'description': '주말 대여가 포함 되는가',
            'in': 'json',
            'type': 'bool',
            'required': True
        },
        {
            'name': 'minBorrowDays',
            'description': '최소 대여 기간',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'maxBorrowDays',
            'description': '최대 대여 기간',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'tradeStartHour',
            'description': '직거래 시작 가능 시간',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'tardeEndHour',
            'description': '직거래 종료 시간',
            'in': 'json',
            'type': 'int',
            'required': True
        },
        {
            'name': 'tradeArea',
            'description': '대여 지역',
            'in': 'json',
            'type': 'str',
            'required': True
        },
        {
            'name': 'tradeAreaX',
            'description': '대여 지역 X좌표',
            'in': 'json',
            'type': 'float',
            'required': True
        },
        {

            'name': 'tradeAreaY',
            'description': '대여 지역 Y좌표',
            'in': 'json',
            'type': 'float',
            'required': True
        },
        {
            'name': 'categories',
            'description': '용품 카테고리',
            'in': 'json',
            'type': 'str',
            'required': True
        }
    ],
    'responses':{
        '201':{
            'description': '대여 등록 성공'
        },
        '400':{
            'description': '오류 발생'
        }
    }
}
SPORROW_CONTENT_GET={
    'tags':['대여'],
    'description':'등록된 대여 용품의 세부 정보 조회',
    'parameters':[
        {
            'name': 'id',
            'description': '페이지 번호',
            'in': 'path',
            'type': 'int',
            'required': True
        }
    ],
    'responses':{
        '204':{
            'description': '페이지가 존재하지 않음'
        },
        '200':{
            'description': '페이지를 찾았고 세부 정보를 반환함',
            'examples':{
                '': {
                    'title': '조민규 운동화 빌려드려요',
                    'owner': '윤석민',
                    'cartCount': 12341,
                    'inMyCart': True,
                    'borrowPrice': 12000,
                    'tradeStartHour': 12,
                    'tradeEndHour': 18,
                    'tradeArea': '대전',
                    'includeWeekend': False
                }
            }
        }
    }
}
SPORROW_CALENDAR_GET={
    'tags': ['대여'],
    'description': '해당 용품의 대여 가능 여부 상태를 담은 캘린더를 반환해줌',
    'parameters': [
        {
            'name': 'id',
            'description': '페이지 번호',
            'in': 'path',
            'type': 'int',
            'required': True
        },
        {
            'name': 'year',
            'description': '년도',
            'in': 'path',
            'type': 'int',
            'required': True
        },
        {
            'name': 'month',
            'description': '달',
            'in': 'path',
            'type': 'int',
            'required': True
        }
    ],
    'responses':{
        '200':{
            'description': '캘린더 반환해줌',
            'examples': {
                '': {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                    '5': 1,
                    '6': 1,
                    '7': 1,
                    '8': 1,
                    '9': 1,
                    '10': 1,
                    '11': 1,
                    '12': 1,
                    '13': 1,
                    '14': 1,
                    '15': 1,
                    '16': 1,
                    '17': 1,
                    '18': 1,
                    '19': 1,
                    '20': 1,
                    '21': 1,
                    '22': 1,
                    '23': 1,
                    '24': 1,
                    '25': 0,
                    '26': 0,
                    '27': 0,
                    '28': 0,
                    '29': 0,
                    '30': 0,
                }
            }
        },
        '204':{
            'description': '페이지 id 오류'
        },
        '400':{
            'description': 'date 오류'
        }
    }
}