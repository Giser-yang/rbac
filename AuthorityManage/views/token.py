from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt import serializers
from rest_framework_simplejwt.views import TokenViewBase


class TokenObtainPairView(TokenViewBase):
    """
    获取token
    """
    serializer_class = serializers.TokenObtainPairSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


token_obtain_pair = TokenObtainPairView.as_view()


class TokenVerifyView(TokenViewBase):
    """
    刷新Token有效期
    """
    serializer_class = serializers.TokenVerifySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


token_verify = TokenVerifyView.as_view()


class TokenRefreshView(TokenViewBase):
    """
    验证Token的有效性
    """
    serializer_class = serializers.TokenRefreshSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


token_refresh = TokenRefreshView.as_view()
