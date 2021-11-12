import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings


def get_token(request):
    #获取用户名、密码
    obj = json.loads(request.body)
    username = obj.get('username', None)
    password = obj.get('password', None)

    if username is None or password is None:
        return JsonResponse({'code': 500, 'message': '请求参数错误'})

    is_login = authenticate(request, username=username, password=password)#测试能否登录
    if is_login is None:
        return JsonResponse({'code': 500, 'message': '账号或密码错误'})

    login(request, is_login)#登录


    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(is_login)#加密的明文字段{'user_id': 4, 'username': 'test', 'exp': datetime.datetime(2021, 11, 11, 9, 51, 15, 259393), '测试属性': 'testtest'}
    token = jwt_encode_handler(payload)#生成token,一般为三段以‘.’隔开，开头是编码方式，中间是base64编码的明文，
    #eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozLCJ1c2VybmFtZSI6InhpYW5ncWk2NjYiLCJleHAiOjE2MzY2MjYyNzAsImVtYWlsIjoieGlhbmdxaUA2NjYuY29tIn0.mQkfiNruPcpPqRB29PfEtrb-v85o6jYWoMohd4hCfcQ
    return JsonResponse(
        {
            'code': 200,
            'message': '登录成功',
            'data': {'token': token}
        }
    )

