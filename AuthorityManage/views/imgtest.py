from django.http import JsonResponse
from drf_yasg.openapi import Parameter, IN_QUERY, IN_PATH, TYPE_INTEGER, TYPE_STRING, IN_BODY, IN_FORM
from drf_yasg.utils import swagger_auto_schema


from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.paginator import Paginator
from AuthorityManage.models import Users, ImgList
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
import logging

logger = logging.getLogger(__name__)


# Create your views here.


# class UserQuerySerialzer(serializers.Serializer):
#     mobile = serializers.CharField(help_text="电话")
#
#     class Meta:
#         fields = '__all__'


class ImgListSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Id")
    name = serializers.CharField(help_text="名称")
    url = serializers.ImageField(help_text="图片路径")
    update_datetime = serializers.DateTimeField(help_text="修改时间")
    create_datetime = serializers.DateTimeField(help_text="创建时间")

    class Meta:
        fields = '__all__'





class ProjectImg(APIView):
    permission_classes = [IsAuthenticated]
    user_view_get_desc = '返回图片数据，测试分页'
    user_view_get_parm = [
        Parameter(name='page', in_=IN_QUERY, description='page', type=TYPE_INTEGER,
                  required=True),
        Parameter(name='limit', in_=IN_QUERY, description='limit', type=TYPE_INTEGER,
                  required=True),
    ]
    user_view_get_resp = {'200': ImgListSerializer,
                          '400': "Bad Request"}

    # @authentication_classes((JWTAuthentication,))   # 设置需要携带token访问
    @swagger_auto_schema(operation_description=user_view_get_desc, manual_parameters=user_view_get_parm,
                         responses=user_view_get_resp, tags=['分页测试功能'])
    def get(self, request, *args, **kwargs):
        """
        通过电话查询用户
        """
        page_number = request.GET['page']
        limit_number = request.GET['limit']
        return_data = ImgList.objects.all()
        paginator = Paginator(return_data, limit_number)
        page_obj = paginator.get_page(page_number)
        return_data1 = ImgListSerializer(instance=page_obj, many=True)
        return_data1 = {
            'code': 200,
            'message': "查询成功",
            'data': return_data1.data
        }
        return JsonResponse(return_data1)