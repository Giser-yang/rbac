# -*- coding: utf-8 -*-

from django.contrib.auth.hashers import make_password
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import Users
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
from AuthorityManage.utils.validator import CustomUniqueValidator


class UserSerializer(serializers.ModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = Users
        read_only_fields = ["id"]
        exclude = ['password']
        extra_kwargs = {
            'post': {'required': False},
        }


class UserCreateSerializer(serializers.Serializer):
    """
    用户新增-序列化器
    """
    username = serializers.CharField(max_length=50,
                                     validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=True)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('post', []))
        return data

    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]
        extra_kwargs = {
            'post': {'required': False},
        }


class UserUpdateSerializer(serializers.Serializer):
    """
    用户修改-序列化器
    """
    username = serializers.CharField(max_length=50,
                                     validators=[CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")])
    password = serializers.CharField(required=False, allow_blank=True)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.post.set(self.initial_data.get('post', []))
        return data

    class Meta:
        model = Users
        read_only_fields = ["id"]
        fields = "__all__"
        extra_kwargs = {
            'post': {'required': False, 'read_only': True},
        }


class UserViewSet(ModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def user_info(self, request):
        """获取当前用户信息"""
        user = request.user
        result = {
            "name": user.name,
            "mobile": user.mobile,
            "gender": user.gender,
            "email": user.email
        }
        return SuccessResponse(data=result, message="获取成功")

    def update_user_info(self, request):
        """修改当前用户信息"""
        user = request.user
        Users.objects.filter(id=user.id).update(**request.data)
        return SuccessResponse(data=None, message="修改成功")

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "oldPassword": openapi.Schema(type=openapi.TYPE_STRING, description='原密码', ),
                "newPassword": openapi.Schema(type=openapi.TYPE_STRING, description='新密码', ),
                "newPassword2": openapi.Schema(type=openapi.TYPE_STRING, description='验证新密码', ),
            },
        )
        , operation_description='修改密码', tags=['修改密码'])
    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        instance = Users.objects.filter(id=kwargs.get('pk')).first()
        data = request.data
        old_pwd = data.get('oldPassword')
        new_pwd = data.get('newPassword')
        new_pwd2 = data.get('newPassword2')
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(message="两次密码不匹配")
            elif instance.check_password(old_pwd):
                instance.password = make_password(new_pwd)
                instance.save()
                return SuccessResponse(data=None, message="修改成功")
            else:
                return ErrorResponse(message="旧密码不正确")
        else:
            return ErrorResponse(message="未获取到用户")
