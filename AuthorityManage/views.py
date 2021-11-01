from django.http import JsonResponse
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema

from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from AuthorityManage.models import Users
from AuthorityManage.utils.permission import CustomPermission


# Create your views here.


# class UserQuerySerialzer(serializers.Serializer):
#     mobile = serializers.CharField(help_text="电话")
#
#     class Meta:
#         fields = '__all__'


class returnUsersModelSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="用户账号")
    email = serializers.EmailField(help_text="邮箱")
    mobile = serializers.CharField(help_text="电话")
    avatar = serializers.ImageField(help_text="头像")
    name = serializers.CharField(help_text="姓名")

    class Meta:
        fields = '__all__'


class ProjectUser(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='mobile',
            in_=openapi.IN_PATH,
            description='电话号码',
            type=openapi.TYPE_INTEGER,
            required=True,
        ),
        openapi.Parameter(
            name='test',
            in_=openapi.IN_PATH,
            description='测试字段',
            type=openapi.TYPE_INTEGER,
            required=True,
        )
    ],
        responses={'200': returnUsersModelSerializer,
                   '400': "Bad Request"},
        tags=['测试功能-用户查询']
    )
    def post(self, request, *args, **kwargs):
        mobile = request.POST['mobile']
        return_data = Users.objects.all()

        return_data1 = returnUsersModelSerializer(instance=return_data, many=True)
        print(return_data1.data)
        return Response(return_data1.data)
