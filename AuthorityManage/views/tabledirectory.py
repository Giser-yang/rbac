from drf_yasg import openapi
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from AuthorityManage.models import Users
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse


class ReturnUserTableSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Id")
    username = serializers.CharField(help_text="用户账号")
    email = serializers.EmailField(help_text="邮箱")
    mobile = serializers.CharField(help_text="电话")
    name = serializers.CharField(help_text="姓名")
    gender = serializers.IntegerField(help_text="性别")
    update_datetime = serializers.DateTimeField(help_text="修改时间")
    create_datetime = serializers.DateTimeField(help_text="创建时间")
    APIToUser = serializers.ListField(help_text="API")
    FileToUser = serializers.ListField(help_text="文件")
    groups = serializers.ListField(help_text="组")


class UserGroup(APIView):
    '''
    用户分组
    '''
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '添加用户至分组'

    user_view_get_resp = {'200': ReturnUserTableSerializer,
                          '400': "Bad Request"}

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "userid": openapi.Schema(type=openapi.TYPE_INTEGER, description='用户Id', ),
            },
        )
        , operation_description=user_view_get_desc, responses=user_view_get_resp, tags=['添加用户至分组'])
    @authentication_classes((JWTAuthentication,))  # 设置需要携带token访问
    def post(self, request, *args, **kwargs):
        """
        添加用户至分组
        """
        data = request.data
        userid = data['userid']
