from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import Users
from rest_framework.serializers import ModelSerializer
from AuthorityManage.utils.permission import CustomPermission
from django_filters.rest_framework import DjangoFilterBackend

class UsersModelSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        read_only_fields = ['id']


class UsersViewSet(ModelViewSet):
    """
        用户管理接口
        list:查询
        create:新增
        update:修改
        retrieve:单例
        destroy:删除
        """
    queryset = Users.objects.all()
    serializer_class = UsersModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ['name', 'username']
    permission_classes = [IsAuthenticatedOrReadOnly]

