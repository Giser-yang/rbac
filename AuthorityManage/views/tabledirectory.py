from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.contenttypes.models import ContentType
from AuthorityManage.utils.json_response import SuccessResponse
from django.db.models import Q
from AuthorityManage.models import Users
from AuthorityManage.views.grouprelated import APISerializer, FileSerializer,PermissionSerializer

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

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        read_only_fields = ["id", 'app_label']
        exclude = []
        extra_kwargs = {}

class ReturnUserTableSerializer(serializers.Serializer):#接口的字段说明
    model_name = serializers.CharField(help_text="模型名称")
    model_verbose_name = serializers.CharField(help_text="模型中文名称")
    fields = serializers.ListField(help_text="字段列表")
    fieldname = serializers.CharField(help_text="字段名称")
    verbose_name = serializers.CharField(help_text="字段别名")
    type = serializers.CharField(help_text="字段类型")


class TableView(APIView):#根据用户权限获取表单目录,字段名/字段类型等
    """
    表单目录
    """
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '根据用户权限获取表单目录'

    user_view_get_resp = {'200': ReturnUserTableSerializer,
                          '400': "Bad Request"}
    @swagger_auto_schema(operation_description=user_view_get_desc, responses=user_view_get_resp, tags=['返回目录'])
    @authentication_classes((JWTAuthentication,))  # 设置需要携带token访问
    def get(self, request, *args, **kwargs):
        user = request.user
        user = Users.objects.get(username=user)
        # 排除条件
        exclude = Q(app_label='authtoken') | Q(app_label='contenttypes') | Q(app_label='sessions') | Q(
            app_label='admin')
        # 如果是超级用户，直接返回所有
        if user.is_superuser:
            table = ContentType.objects.filter().exclude(exclude)
        else:
            permissions = user.get_all_permissions()
            # 模型名称列表
            permissions_1 = set()
            for item in permissions:
                permission_name = item.split('.')
                permissions_1.add(permission_name[1].split('_')[1])
            query = Q()
            for permission in permissions_1:
                query.add(Q(model=permission), Q.OR)
            table = ContentType.objects.filter(query).exclude(exclude)
        data = TableSerializer(instance=table, many=True).data
        res=[]
        for i in data:
            # temp=[]
            app_label = i['app_label']
            modelname = i ['model']
            model2 = str(ContentType.objects.get(app_label=app_label,model=modelname)).split('|')#模型中文名
            # fields = ContentType.objects.get(app_label=app_label,model=modelname).model_class()._meta.fields#模型字段列表
            # for j in  fields:
            #     field={
            #         'fieldname':j.name,#字段名
            #         'verbose_name':j.verbose_name,#字段别名
            #         # 'type':type(j).__name__#字段类型
            #     }
            #     temp.append(field)
            res.append({
                "model_name":modelname,
                "model_verbose_name": model2[1].replace(' ', ''),#模型别名
                # "fields": temp
            })
        return SuccessResponse(data=res, message="返回成功")

