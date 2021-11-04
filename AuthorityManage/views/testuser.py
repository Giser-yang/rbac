from django.http import JsonResponse
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH, TYPE_INTEGER, TYPE_STRING, IN_BODY, IN_FORM
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from AuthorityManage.models import Users
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import logging
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
logger = logging.getLogger(__name__)


# Create your views here.


# class UserQuerySerialzer(serializers.Serializer):
#     mobile = serializers.CharField(help_text="电话")
#
#     class Meta:
#         fields = '__all__'


class returnUsersModelSerializer(serializers.Serializer):
    code = serializers.IntegerField(help_text="返回码")
    userid = serializers.IntegerField(help_text="用户id")
    message = serializers.CharField(help_text="描述信息")

    class Meta:
        fields = '__all__'


class Users1(serializers.Serializer):
    id = serializers.IntegerField(help_text="Id")
    username = serializers.CharField(help_text="用户账号")
    email = serializers.EmailField(help_text="邮箱")
    mobile = serializers.CharField(help_text="电话")
    avatar = serializers.ImageField(help_text="头像")
    gender = serializers.IntegerField(help_text="性别")
    update_datetime = serializers.DateTimeField(help_text="修改时间")
    create_datetime = serializers.DateTimeField(help_text="创建时间")

    class Meta:
        db_table = "system_users"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('create_datetime',)


class ProjectUser(APIView):
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '根据电话号码返回数据'
    user_view_get_parm = [
        Parameter(name='mobile', in_=IN_QUERY, description='电话号码 example:17760485080', type=TYPE_STRING,
                  required=True),
        Parameter(name='page', in_=IN_QUERY, description='page', type=TYPE_INTEGER,
                  required=True),
        Parameter(name='limit', in_=IN_QUERY, description='limit', type=TYPE_INTEGER,
                  required=True),
    ]
    user_view_get_resp = {'200': Users1,
                          '400': "Bad Request"}

    @authentication_classes((JWTAuthentication,))   # 设置需要携带token访问
    @swagger_auto_schema(operation_description=user_view_get_desc, manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['测试用户功能'])
    def get(self, request, *args, **kwargs):
        """
        通过电话查询用户
        """
        mobile = request.GET['mobile']
        page_number = request.GET['page']
        limit_number = request.GET['limit']
        # return_data = Users.objects.filter(mobile=mobile)
        return_data = Users.objects.filter(mobile=mobile)
        paginator = Paginator(return_data, limit_number)
        page_obj = paginator.get_page(page_number)
        return_data1 = Users1(instance=page_obj, many=True)
        return SuccessResponse(data=return_data1.data, message="查询成功")

    user_view_get_desc = '新增用户'
    user_view_get_resp = {'200': returnUsersModelSerializer,
                          '400': "Bad Request"}

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(type=openapi.TYPE_STRING, description='用户账号 example:张三', ),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description='密码 example:12345678', ),
                "gender": openapi.Schema(type=openapi.TYPE_INTEGER, description='性别 例如：1 代表男性，0代表女性', enum=[0, 1]),
                "is_superuser": openapi.Schema(type=openapi.TYPE_INTEGER, description='是否超级用户 例如：1 是，0 否', enum=[0, 1]),
            },
        )
        , operation_description=user_view_get_desc, responses=user_view_get_resp, tags=['测试新增用户功能'])
    def post(self, request, *args, **kwargs):
        """
        新增用户
        """
        data = request.data
        print(data)
        username = data['username']
        password = data['password']
        gender = int(data['gender'])
        # name = request.POST['name']
        is_superuser = int(data['is_superuser'])
        dictinfo = {
            "username": username,
            "password": password,
            "gender": gender,
            # "name": name,
            "is_superuser": is_superuser,
            "is_staff": 1
        }
        use1 = Users.objects.create_user(**dictinfo)
        use1.save()
        return_data = {
            'code': 200,
            'userid': use1.id,
            'message': "用户创建成功",
        }
        return JsonResponse(return_data)
