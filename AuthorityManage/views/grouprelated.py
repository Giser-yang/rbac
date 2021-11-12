import datetime

from django.contrib.auth.models import Permission, Group , User
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action, authentication_classes
from rest_framework.viewsets import ViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
from AuthorityManage.models import Groups,ImgList,FileManage,APIManage,OperationLog,Users
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
        for apipermission in user_obj.apitouser.all():
            serializer = APISerializer(apipermission)
            apipermissions_list.append(serializer.data)
        return apipermissions_list

    def get_user_file_permission(self, user_obj):#通过中间表获取file权限
        filepermissions_list = list()
        for filepermission in user_obj.filetouser.all():
            serializer = FileSerializer(filepermission)
            filepermissions_list.append(serializer.data)
        return filepermissions_list

    # 自定义多字段验证方法
    def validate(self, attrs):
        return attrs

class PermissionSerializer(serializers.Serializer):#系统权限的序列化器
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]
    id = serializers.ReadOnlyField()#id字段不作操作，但是会返回在结果中
    name = serializers.CharField(min_length=1)
    content_type_id = serializers.IntegerField()
    codename = serializers.CharField(min_length=1)

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class APISerializer(serializers.Serializer):#api接口序列化器
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]
    id = serializers.ReadOnlyField()#id字段不作操作，但是会返回在结果中
    APItype = serializers.CharField(max_length=200,allow_null=True,read_only=True, help_text="接口类型")
    name = serializers.CharField(max_length=50, allow_null=True,read_only=True,   help_text="名称")
    url = serializers.CharField(max_length=200,allow_null=True, read_only=True, help_text="路由地址")
    update_datetime = serializers.DateTimeField(read_only=True,allow_null=True,  help_text="修改时间")
    create_datetime = serializers.DateTimeField(read_only=True, allow_null=True, help_text="创建时间")

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class FileSerializer(serializers.Serializer):#file接口序列化器
    class Meta:
        model = Permission
        fields = "__all__"
        read_only_fields = ["id"]
    id = serializers.ReadOnlyField()#id字段不作操作，但是会返回在结果中
    filetype  = serializers.CharField(max_length=200,allow_null=True,read_only=True, help_text="文件类型")
    name = serializers.CharField(max_length=50, allow_null=True,read_only=True,   help_text="名称")
    path = serializers.CharField(max_length=200,  allow_null=True, read_only=True, help_text="文件路径")
    update_datetime = serializers.DateTimeField(read_only=True,allow_null=True,  help_text="修改时间")
    create_datetime = serializers.DateTimeField(read_only=True, allow_null=True, help_text="创建时间")

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

class GroupSerializer(serializers.Serializer):#组的序列化器
    class Meta:
        model = Groups
        fields = "__all__"
        read_only_fields = ["id"]

    update_datetime=serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True ,default=datetime.datetime.now())
    create_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True )
    id = serializers.ReadOnlyField(help_text='组的id')#
    name = serializers.CharField(help_text='组名')#
    apitouser = serializers.SerializerMethodField(help_text='api权限列表')
    filetouser = serializers.SerializerMethodField(help_text='file权限列表')
    authpermissions = serializers.SerializerMethodField(help_text='管理权限列表')

    def get_authpermissions(self,group_obj):
        permissions_list = list()
        for permission in group_obj.permissions.all():
            serializer = PermissionSerializer(permission)
            permissions_list.append(serializer.data)
        return permissions_list
    def get_apitouser(self,group_obj):
        apipermissions_list = list()
        for apipermission in group_obj.apitouser.all():
            serializer = APISerializer(apipermission)
            apipermissions_list.append(serializer.data)
        return apipermissions_list
    def get_filetouser(self,group_obj):
        filepermissions_list = list()
        for filepermission in group_obj.filetouser.all():
            serializer = FileSerializer(filepermission)
            filepermissions_list.append(serializer.data)
        return filepermissions_list

    # 定义多字段验证方法
    def validate(self, attrs):
        return attrs

    # 定义保存方法
    def create(self, validated_data):
        from django.contrib.auth.models import Permission, Group , User
        group = Group.objects.create(name=validated_data['name'])
        return group

    # 定义更新方法
    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        # permissions需要单独写 todo
        instance.save()
        return instance

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
                haspermissions = serializer.data['authpermissions']
                tempauth['haspermissions']=haspermissions
                for j in  authallpermissions:
                    if j not in haspermissions:
                        nopermissions.append(j)
                tempauth['nopermissions']=nopermissions
                nopermissions=[]
                res['authpermissions']=tempauth

                # 获取api权限
                tempapi={}
                haspermissions = serializer.data['apitouser']
                tempapi['haspermissions'] = haspermissions
                for j in apiallpermissions:
                    if j not in haspermissions:
                        nopermissions.append(j)
                tempapi['nopermissions'] = nopermissions
                nopermissions = []
                res['apipermissions'] = tempapi
                # 获取文件权限
                tempfile={}
                haspermissions = serializer.data['filetouser']
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
    def groupupdatepermissions1(self, request, *args, **kwargs):
        data = request.data

        #验证是否有该接口的权限
        username = request.user
        userserializer = UserSerializer(username)
        haspermission = 0
        for i in userserializer.data['user_api_permission']:
            if i['url'] ==request.path:#判断url是否相等，若有相等的
                haspermission = 1
                break
        if haspermission==0:
            return ErrorResponse('该用户无权限')

        groupid = data['groupid']
        group = Groups.objects.filter(id=groupid)
        if not group:
            return ErrorResponse('组不存在')
        group = group[0]

        # 系统权限更新
        authpermissions = data['authpermissions'].split(',')  # 需要保存的权限，文本
        authneedsavepermissions = Permission.objects.filter(id__in=authpermissions)#获取要保存的所有权限
        #两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        #判断法
        authhaspermissions=group.permissions.all()
        addarr=[]
        deletearr=[]
        for i in authneedsavepermissions:#不在的新增
            if i not in authhaspermissions:
                addarr.append(i)
        for  i in authhaspermissions:
            if i not in authneedsavepermissions:#不在的移除
                deletearr.append((i))
        group.permissions.add(*addarr)#添加所有关联
        group.permissions.remove(*deletearr)

        #直接删除法
        # group.permissions.clear()#删除所有关联
        # group.permissions.add(*needsavepermissions)#添加所有关联

        # api权限更新
        apipermissions = data['apipermissions'].split(',')  # 需要保存的权限，文本
        apineedsavepermissions = APIManage.objects.filter(id__in=apipermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        apihaspermissions = group.apitouser.all()
        addarr = []
        deletearr = []
        for i in apineedsavepermissions:  # 不在的新增
            if i not in apihaspermissions:
                addarr.append(i)
        for i in apihaspermissions:
            if i not in apineedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.apitouser.add(*addarr)  # 添加所有关联
        group.apitouser.remove(*deletearr)

        # 直接删除法
        # group.apitouser.clear()#删除所有关联
        # group.apitouser.add(*apineedsavepermissions)#添加所有关联

        # file权限更新
        filepermissions = data['filepermissions'].split(',')  # 需要保存的权限，文本
        fileneedsavepermissions = FileManage.objects.filter(id__in=filepermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        filehaspermissions = group.filetouser.all()
        addarr = []
        deletearr = []
        for i in fileneedsavepermissions:  # 不在的新增
            if i not in filehaspermissions:
                addarr.append(i)
        for i in filehaspermissions:
            if i not in fileneedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.filetouser.add(*addarr)  # 添加所有关联
        group.filetouser.remove(*deletearr)

        # 直接删除法
        # group.apitouser.clear()#删除所有关联
        # group.apitouser.add(*apineedsavepermissions)#添加所有关联

        groupserializer = GroupSerializer(group)

        return SuccessResponse(groupserializer.data)

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

        # 直接删除法
        # group.permissions.clear()#删除所有关联
        # group.permissions.add(*needsavepermissions)#添加所有关联

        # api权限更新
        apipermissions = data['apipermissions'].split(',')  # 需要保存的权限，文本
        apineedsavepermissions = APIManage.objects.filter(id__in=apipermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        apihaspermissions = group.apitouser.all()
        addarr = []
        deletearr = []
        for i in apineedsavepermissions:  # 不在的新增
            if i not in apihaspermissions:
                addarr.append(i)
        for i in apihaspermissions:
            if i not in apineedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.apitouser.add(*addarr)  # 添加所有关联
        group.apitouser.remove(*deletearr)

        # 直接删除法
        # group.apitouser.clear()#删除所有关联
        # group.apitouser.add(*apineedsavepermissions)#添加所有关联

        # file权限更新
        filepermissions = data['filepermissions'].split(',')  # 需要保存的权限，文本
        fileneedsavepermissions = FileManage.objects.filter(id__in=filepermissions)  # 获取要保存的所有权限
        # 两种方式更新，一种直接全删除再插入，一种判断哪些删除，哪些插入
        # 判断法
        filehaspermissions = group.filetouser.all()
        addarr = []
        deletearr = []
        for i in fileneedsavepermissions:  # 不在的新增
            if i not in filehaspermissions:
                addarr.append(i)
        for i in filehaspermissions:
            if i not in fileneedsavepermissions:  # 不在的移除
                deletearr.append((i))
        group.filetouser.add(*addarr)  # 添加所有关联
        group.filetouser.remove(*deletearr)

        # 直接删除法
        # group.apitouser.clear()#删除所有关联
        # group.apitouser.add(*apineedsavepermissions)#添加所有关联

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
