from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from AuthorityManage.models import Users
from django.contrib.auth.models import Group
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse


class ReturnUserPermissionSerializer(serializers.Serializer):
    user_table_permission = serializers.ListField(help_text="系统表操作权限")
    user_api_permission = serializers.ListField(help_text="API接口访问权限")
    user_file_permission = serializers.ListField(help_text="文件访问权限")


class UserPermission(APIView):
    permission_classes = [IsAuthenticated]
    user_view_get_resp = {"200": ReturnUserPermissionSerializer,
                          '400': "Bad Request"}

    user_view_get_parm = [
        Parameter(name='id', in_=IN_PATH, description='Id', type=openapi.TYPE_STRING,
                  required=True),
    ]

    @swagger_auto_schema(operation_description="用户权限", manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['权限'])
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        user = Users.objects.get(id=id)
        return_data = {
            "user_table_permission": user.get_user_permissions(),
            "user_api_permission": [],
            "user_file_permission": [],
        }
        return SuccessResponse(data=return_data, message="")


class GroupPermission(APIView):
    permission_classes = [IsAuthenticated]
    user_view_get_resp = {"200": ReturnUserPermissionSerializer,
                          '400': "Bad Request"}

    user_view_get_parm = [
        Parameter(name='id', in_=IN_PATH, description='Id', type=openapi.TYPE_STRING,
                  required=True),
    ]

    @swagger_auto_schema(operation_description="组权限", manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['权限'])
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        group = Group.objects.get(id=id)
        return_data = {
            "group_table_permission": group.get_all_permissions(),
            "group_api_permission": [],
            "group_file_permission": [],
        }
        return SuccessResponse(data=return_data, message="")
