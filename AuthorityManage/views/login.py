# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/2 002 14:20
@Remark:登录视图
"""
import base64
import hashlib
from datetime import datetime, timedelta
from django.contrib import auth
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from AuthorityManage.models import Users
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse


class LoginSerializer(TokenObtainPairSerializer):
    """
    登录的序列化器:
    重写djangorestframework-simplejwt的序列化器
    """

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]

    default_error_messages = {
        'no_active_account': _('该账号已被禁用,请联系管理员')
    }

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        user = Users.objects.filter(username=username).first()
        if user and user.check_password(password):
            data = super().validate(attrs)
            refresh = self.get_token(self.user)
            data['name'] = self.user.name
            data['userId'] = self.user.id
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
            result = {
                "code": 200,
                "message": "请求成功",
                "data": data
            }
        else:
            result = {
                "code": 400,
                "message": "账号/密码不正确",
                "data": None
            }
        return result


class LoginView(TokenObtainPairView):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ApiLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = ['username', 'password']


# class ApiLogin(APIView):
#     """接口文档的登录接口"""
#     serializer_class = ApiLoginSerializer
#
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user_obj = auth.authenticate(request, username=username, password=password)
#         if user_obj:
#             return redirect('/')
#         else:
#             return ErrorResponse(msg="账号/密码错误")
