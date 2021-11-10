from drf_yasg import openapi
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.contenttypes.models import ContentType
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse
from django.db.models import Q
from AuthorityManage.models import Users


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentType
        read_only_fields = ["id", 'app_label']
        exclude = []
        extra_kwargs = {}


class TableView(APIView):
    """
    表单目录
    """
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '根据用户权限获取表单目录'

    user_view_get_resp = {'200': 'ReturnUserTableSerializer',
                          '400': "Bad Request"}

    @swagger_auto_schema(operation_description=user_view_get_desc, responses=user_view_get_resp, tags=['返回目录'])
    @authentication_classes((JWTAuthentication,))  # 设置需要携带token访问
    def get(self, request, *args, **kwargs):
        """
        表单目录
        """
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
            print(permissions_1)
        data = TableSerializer(instance=table, many=True)
        fields = ContentType.objects.get(model='apimanage').model_class()._meta.fields
        print(ContentType.objects.get(model='apimanage').model_class())
        print(ContentType.objects.get(model='apimanage'))
        print(fields)
        for i in fields:
            print(i.name, i.verbose_name)
        return SuccessResponse(data=data.data, message="返回成功")
