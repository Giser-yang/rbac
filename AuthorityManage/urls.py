from django.urls import path, re_path
from rest_framework import routers

from AuthorityManage.views.login import LoginView

system_url = routers.SimpleRouter()

from AuthorityManage.system.img_list import ImgViewSet
from AuthorityManage.system.user import UserViewSet


system_url.register(r'img', ImgViewSet)
system_url.register(r'user', UserViewSet)

from AuthorityManage.views.token import TokenObtainPairView, TokenVerifyView, TokenRefreshView
urlpatterns = [
    # 获取Token的接口
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),

    # path(r'project', ProjectUser.as_view()),
    path('user/user_info/', UserViewSet.as_view({'get': 'user_info', 'put': 'update_user_info'})),
    re_path('user/change_password/(?P<pk>.*?)/', UserViewSet.as_view({'put': 'change_password'})),
    # path(r'projectimg', ProjectImg.as_view()),
    # path(r'token', GetToken.as_view()),

]
urlpatterns += system_url.urls
