from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH, TYPE_STRING
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from AuthorityManage.models import Users, Groups
from django.contrib.auth.models import  Permission
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
from AuthorityManage.views.grouprelated import APISerializer, FileSerializer, GroupSerializer, PermissionSerializer


class ReturnUserPermissionSerializer(serializers.Serializer):
    user_table_permission = serializers.ListField(help_text="系统表操作权限")
    user_api_permission = serializers.ListField(help_text="API接口访问权限")
    user_file_permission = serializers.ListField(help_text="文件访问权限")
    group = serializers.ListField(help_text="组")


class UserSerializer(serializers.ModelSerializer):  # 用户的序列化器
    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
    APIToUser = serializers.SerializerMethodField(help_text='api权限列表')
    FileToUser = serializers.SerializerMethodField(help_text='file权限列表')
    user_table_permission = serializers.SerializerMethodField(help_text='系统权限')
    group_id = serializers.CharField(read_only=True, source="group.id")
    group_name = serializers.CharField(read_only=True, source="group.name")
    #
    def get_APIToUser(self, group_obj):
        apipermissions_list = list()
        for apipermission in group_obj.APIToUser.all():
            serializer = APISerializer(apipermission)
            apipermissions_list.append(serializer.data)
        return apipermissions_list

    def get_FileToUser(self, group_obj):
        filepermissions_list = list()
        for filepermission in group_obj.FileToUser.all():
            serializer = FileSerializer(filepermission)
            filepermissions_list.append(serializer.data)
        return filepermissions_list
    #
    def get_user_table_permission(self, user_obj):#通过中间表获取系统权限
        authpermissions_list = list()
        for apipermission in user_obj.user_permissions.all():
            serializer = PermissionSerializer(apipermission)
            authpermissions_list.append(serializer.data)
        return authpermissions_list

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class UserPermission(APIView):
    #获取用户权限
    permission_classes = [IsAuthenticated]
    user_view_get_resp = {"200": ReturnUserPermissionSerializer,
                          '400': "Bad Request"}
    user_view_get_parm = [
        Parameter(name='id', in_=IN_PATH, description='用户Id', type=openapi.TYPE_STRING,
                  required=True),
    ]
    @swagger_auto_schema(operation_description="用户权限", manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['权限'])
    @authentication_classes((JWTAuthentication,))
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        try:
            user = Users.objects.get(id=id)
        except:
            return ErrorResponse('该用户不存在！')
        serializer = UserSerializer(user)
        res = serializer.data
        # authpermissions=''
        authpermissions = user.get_user_permissions()#获取用户的系统权限
        res['user_table_permission'] = authpermissions
        return_data = {
            "user_table_permission": authpermissions,
            "user_api_permission": res['APIToUser'],#api接口
            "user_file_permission": res['FileToUser'],#文件接口
            "group": {#组
                'group_id':res["group_id"],
                'group_name':res['group_name']
            }
        }
        return SuccessResponse(data=return_data, message="")


class GroupPermission(ViewSet):
    permission_classes = [IsAuthenticated]
    user_view_get_resp = {"200": ReturnUserPermissionSerializer,
                          '400': "Bad Request"}
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    user_view_get_parm = [
        Parameter(name='groupid', in_=IN_QUERY, description='组id', type=TYPE_STRING,
                  required=True),
    ]
    @swagger_auto_schema(operation_description="组权限", manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['权限'])
    @authentication_classes((JWTAuthentication,))
    @action(methods=['get'], detail=False,url_name="组权限")
    def grouppermission(self, request, *args, **kwargs):
        groupid = request.GET['groupid']
        try:
            group = Groups.objects.get(id=groupid)#获取group对象
        except :
            return ErrorResponse('组不存在')
        res = {}
        if group:
            serializer = GroupSerializer(group)
            # 获取系统权限
            haspermissions = serializer.data['permissions']
            res['group_table_permission'] = haspermissions
            # 获取api权限
            haspermissions = serializer.data['APIToGroups']
            res['group_api_permission'] = haspermissions
            # 获取文件权限
            haspermissions = serializer.data['FileToGroups']
            res['group_file_permission'] = haspermissions
        return SuccessResponse(data=res, message="")

class TablepermissionView(ViewSet):
    """
    返回用户对于某表的权限
    """
    queryset = Users.objects.all()#必须有的属性，
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '根据用户权限和表获取表权限'
    user_view_get_resp = {'200': '',
                          '400': "Bad Request"}
    @swagger_auto_schema(operation_description=user_view_get_desc,
                         manual_parameters=[
                             Parameter(name='table_name', in_=IN_QUERY, description='表名称', type=TYPE_STRING,
                                       required=True),
                         ],
                         responses=user_view_get_resp, tags=['权限'])
    @authentication_classes((JWTAuthentication,))
    @action(methods=['get'], detail=False)
    def tablepermission(self, request, *args, **kwargs):
        table_name = request.GET['table_name']#获取表名
        user = request.user
        user = Users.objects.get(username=user)
        # # 排除条件
        exclude = Q(app_label='authtoken') | Q(app_label='contenttypes') | Q(app_label='sessions') | Q(
            app_label='admin')

        #获取表名对应的 content_type_id
        table = ContentType.objects.filter(model=table_name).exclude(exclude)
        content_type_id = table.values()[0]['id']

        if table:
            if user.is_superuser:  # 超级用户返回所有权限
                authpermission = Permission.objects.filter(content_type_id=content_type_id)#根据id获取权限列表
                authpermissionserializer = PermissionSerializer(authpermission, many=True)
                return SuccessResponse(data=authpermissionserializer.data, message="返回成功")
            userserializer = UserSerializer(user)#如果不是管理员，先获取用户对象，序列化
            temp=[]
            #获取系统权限列表
            user_table_permission=userserializer.data['user_table_permission']#这个user_table_permission是序列化器中的自定义字段
            for i in user_table_permission:
                if i['content_type_id']==content_type_id:#找出content_type_id相同的为结果
                    temp.append(i)
            if temp:#列表中是否有权限
                res = {
                    'user_table_permission': temp
                }
                return SuccessResponse(res, message="返回成功")
            else:
                return ErrorResponse("该用户无权限")
        else:
            return ErrorResponse("该用户无权限或者表不存在")

