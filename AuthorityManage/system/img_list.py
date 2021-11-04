from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from AuthorityManage.models import ImgList
from rest_framework.serializers import ModelSerializer


class ImgModelSerializer(ModelSerializer):
    img = serializers.SerializerMethodField(read_only=True)

    def get_img(self, instance):
        return str(instance.url)

    class Meta:
        model = ImgList
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        validated_data['name'] = str(validated_data.get('url'))
        return ImgList.objects.create(**validated_data)


class ImgViewSet(ModelViewSet):
    """
    图片接口
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

