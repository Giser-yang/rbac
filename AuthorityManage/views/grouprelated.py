from django.contrib.auth.models import Permission
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action, authentication_classes
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
from AuthorityManage.models import Groups,FileManage,APIManage,Users
from drf_yasg import openapi
from drf_yasg.openapi import Parameter, IN_QUERY, TYPE_STRING
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import  IsAuthenticatedOrReadOnly

class UserSerializer(serializers.ModelSerializer):  # 组的序列化器
    class Meta:
        model = Users
        fields = "__all__"
        read_only_fields = ["id"]
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    user_api_permission = serializers.SerializerMethodField(help_text='api权限列表')
    user_file_permission = serializers.SerializerMethodField(help_text='file权限列表')
    user_table_permission = serializers.SerializerMethodField(help_text='系统权限')

    def get_user_table_permission(self, user_obj):#通过中间表获取系统权限
        authpermissions_list = list()
        for apipermission in user_obj.user_permissions.all():
            serializer = PermissionSerializer(apipermission)
            authpermissions_list.append(serializer.data)
        return authpermissions_list

    def get_user_api_permission(self, user_obj):#通过中间表获取api权限
        apipermissions_list = list()
        for apipermission in user_obj.APIToUser.all():
            serializer = APISerializer(apipermission)
            apipermissions_list.append(serializer.data)
        return apipermissions_list

    def get_user_file_permission(self, user_obj):#通过中间表获取file权限
        filepermissions_list = list()
        for filepermission in user_obj.FileToUser.all():
            serializer = FileSerializer(filepermission)
            filepermissions_list.append(serializer.data)
        return filepermissions_list

    # 自定义多字段验证方法
    def validate(self, attrs):
        return attrs

class PermissionSerializer(serializers.ModelSerializer):#系统权限的序列化器
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]
    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class APISerializer(serializers.ModelSerializer):#api接口序列化器
    class Meta:
        model = APIManage
        fields = "__all__"
        read_only_fields = ["id"]
    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class FileSerializer(serializers.ModelSerializer):#file接口序列化器
    class Meta:
        model = FileManage
        fields = "__all__"
        read_only_fields = ["id"]

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class GroupSerializer(serializers.ModelSerializer):#组的序列化器
    class Meta:
        model = Groups
        fields = "__all__"
        read_only_fields = ["id"]
    APIToGroups = serializers.SerializerMethodField(help_text='api权限列表')
    FileToGroups = serializers.SerializerMethodField(help_text='file权限列表')
    permissions = serializers.SerializerMethodField(help_text='管理权限列表')

    def get_permissions(self,group_obj):
        permissions_list = list()
        for permission in group_obj.permissions.all():
            serializer = PermissionSerializer(permission)
            permissions_list.append(serializer.data)
        return permissions_list
    def get_APIToGroups(self,group_obj):
        apipermissions_list = list()
        for apipermission in group_obj.APIToGroups.all():
            serializer = APISerializer(apipermission)
            apipermissions_list.append(serializer.data)
        return apipermissions_list
    def get_FileToGroups(self,group_obj):
        filepermissions_list = list()
        for filepermission in group_obj.FileToGroups.all():
            serializer = FileSerializer(filepermission)
            filepermissions_list.append(serializer.data)
        return filepermissions_list

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class Group1(ViewSet):
    '''
    组接口
    '''
    user_view_get_resp = {'200': GroupSerializer,
                          '400': "Bad Request"}
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    @swagger_auto_schema(
        operation_description = '查询某一个组的权限',
        manual_parameters=[
            Parameter(name='groupid', in_=IN_QUERY, description='组id', type=TYPE_STRING,
                      required=True),
        ],
        tags=['group'],
        responses=user_view_get_resp
    )
    @authentication_classes((JWTAuthentication,))
    @action(methods=['get'], detail=False)
    def getgroupnopermissions(self,request, *args, **kwargs):
        #获取组
        groupid = request.GET['groupid']
        group=Groups.objects.filter(id=groupid)
        if not group:
            return  ErrorResponse('组不存在')

        #获取所有权限,auth_permission
        authpermissions = Permission.objects.all()#系统默认权限
        authpermissionsserializer = PermissionSerializer(authpermissions,many=True)

        apipermissions = APIManage.objects.all()#api使用权限
        apipermissionsserializer = APISerializer(apipermissions,many=True)

        filepermissions = FileManage.objects.all()  # file使用权限
        filepermissionsserializer = FileSerializer(filepermissions, many=True)

        authallpermissions = authpermissionsserializer.data
        apiallpermissions = apipermissionsserializer.data
        fileallpermissions = filepermissionsserializer.data

        res={}
        nopermissions=[]
        if group:
            for i in group:#遍历组，根据id查的时候只有一个组
                serializer = GroupSerializer(i)
                # 获取系统权限
                tempauth = {}
                haspermissions = serializer.data['permissions']
                tempauth['haspermissions']=haspermissions
                for j in  authallpermissions:
                    if j not in haspermissions:
                        nopermissions.append(j)
                tempauth['nopermissions']=nopermissions
                nopermissions=[]
                res['authpermissions']=tempauth

                # 获取api权限
                tempapi={}
                haspermissions = serializer.data['APIToGroups']
                tempapi['haspermissions'] = haspermissions
                for j in apiallpermissions:
                    if j not in haspermissions:
                        nopermissions.append(j)
                tempapi['nopermissions'] = nopermissions
                nopermissions = []
                res['apipermissions'] = tempapi
                # 获取文件权限
                tempfile={}
                haspermissions = serializer.data['FileToGroups']
                tempfile['haspermissions'] = haspermissions
                for j in fileallpermissions:
                    if j not in haspermissions:
                        nopermissions.append(j)
                tempfile['nopermissions'] = nopermissions
                nopermissions = []
                res['filepermissions'] = tempfile
        return SuccessResponse(res)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['groupid', 'permissionsid'],
            properties={
                "groupid": openapi.Schema(type=openapi.TYPE_STRING, description='组id example:1'),
                "authpermissions": openapi.Schema(type=openapi.TYPE_STRING,
                                                  description='系统权限id example:1'),
                "apipermissions": openapi.Schema(type=openapi.TYPE_STRING,
                                                 description='api权限id example:1,2'),
                "filepermissions": openapi.Schema(type=openapi.TYPE_STRING,
                                                  description='file权限id example:1,2,3'),
            },
        )
        , operation_description='保存权限', tags=['group'],
        responses=user_view_get_resp)
    @authentication_classes((JWTAuthentication,))
    @action(methods=['post'], detail=False)
    def groupupdatepermissions(self, request, *args, **kwargs):
        data = request.data
        groupid = data['groupid']
        group = Groups.objects.filter(id=groupid)
        if not group:
            return ErrorResponse('组不存在')
        group = group[0]

        # 系统权限更新
        authpermissions = data['authpermissions'].split(',')  # 需要保存的权限，文本
        authneedsavepermissions = Permission.objects.filter(id__in=authpermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        authhaspermissions = group.permissions.all()
        addarr = []
        deletearr = []
        for i in authneedsavepermissions:  # 不在的新增
            if i not in authhaspermissions:
                addarr.append(i)
        for i in authhaspermissions:
            if i not in authneedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.permissions.add(*addarr)  # 添加所有关联
        group.permissions.remove(*deletearr)

        # api权限更新
        apipermissions = data['apipermissions'].split(',')  # 需要保存的权限，文本
        apineedsavepermissions = APIManage.objects.filter(id__in=apipermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        apihaspermissions = group.APIToGroups.all()
        addarr = []
        deletearr = []
        for i in apineedsavepermissions:  # 不在的新增
            if i not in apihaspermissions:
                addarr.append(i)
        for i in apihaspermissions:
            if i not in apineedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.APIToGroups.add(*addarr)  # 添加所有关联
        group.APIToGroups.remove(*deletearr)

        # file权限更新
        filepermissions = data['filepermissions'].split(',')  # 需要保存的权限，文本
        fileneedsavepermissions = FileManage.objects.filter(id__in=filepermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        filehaspermissions = group.FileToGroups.all()
        addarr = []
        deletearr = []
        for i in fileneedsavepermissions:  # 不在的新增
            if i not in filehaspermissions:
                addarr.append(i)
        for i in filehaspermissions:
            if i not in fileneedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.FileToGroups.add(*addarr)  # 添加所有关联
        group.FileToGroups.remove(*deletearr)


        groupserializer = GroupSerializer(group)

        return SuccessResponse(groupserializer.data)


class GroupViewSet(ModelViewSet):
    """
    组接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Groups.objects.all()
    serializer_class = GroupSerializer
    filter_fields = ['name', ]
    search_fields = ('name', )
    permission_classes = [IsAuthenticatedOrReadOnly]
