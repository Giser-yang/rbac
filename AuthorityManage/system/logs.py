from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import OperationLog
from rest_framework.serializers import ModelSerializer


class LogModelSerializer(ModelSerializer):

    class Meta:
        model = OperationLog
        fields = '__all__'
        read_only_fields = ['id']


class LogViewSet(ModelViewSet):
    """
    日志接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = OperationLog.objects.all()
    serializer_class = LogModelSerializer
    # filter_fields = ['request_path', ]    # 精确匹配
    search_fields = ('request_path', )  # 模糊查询
    permission_classes = [IsAuthenticatedOrReadOnly]

