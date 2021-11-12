import time
import base64
import hmac

from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.response import Response

from AuthorityManage.models import Users, Groups

from rest_framework.authentication import BaseAuthentication
from AuthorityManage import models
from rest_framework.exceptions import NotAuthenticated
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from AuthorityManage.utils.json_response import SuccessResponse

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

