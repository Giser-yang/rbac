from rest_framework import serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import Groups
from rest_framework.serializers import ModelSerializer


class GroupModelSerializer(ModelSerializer):

    class Meta:
        model = Groups
        fields = '__all__'
        read_only_fields = ['id']


class GroupViewSet(ModelViewSet):
    """
    用户分组接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Groups.objects.all()
    serializer_class = GroupModelSerializer
    # filter_fields = ['request_path', ]    # 精确匹配
    search_fields = ('name', )  # 模糊查询
    permission_classes = [IsAuthenticatedOrReadOnly]

