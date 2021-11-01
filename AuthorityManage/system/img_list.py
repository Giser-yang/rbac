from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import ImgList
from rest_framework.serializers import ModelSerializer
from AuthorityManage.utils.permission import CustomPermission


class ImgModelSerializer(ModelSerializer):
    class Meta:
        model = ImgList
        fields = '__all__'
        read_only_fields = ['id']


class ImgViewSet(ModelViewSet):
    """
    图片管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ImgList.objects.all()
    serializer_class = ImgModelSerializer
    filter_fields = ['name', ]
    search_fields = ('name', )
    permission_classes = [IsAuthenticatedOrReadOnly]

