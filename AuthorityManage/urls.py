from django.urls import path, re_path
from rest_framework import routers

from AuthorityManage import views
from AuthorityManage.views.login import LoginView
app_name="AuthorityManage"
system_url = routers.SimpleRouter()

from AuthorityManage.system.img_list import ImgViewSet
from AuthorityManage.system.user import UserViewSet
from AuthorityManage.system.logs import LogViewSet
from AuthorityManage.views.grouprelated import Group1,GroupViewSet
from AuthorityManage.views.get_permission import UserPermission,GroupPermission,TablepermissionView#查询权限相关，用户权限/组权限/用户的模型权限
from AuthorityManage.views.tokentest import get_token
system_url.register(r'img', ImgViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'logs', LogViewSet)
system_url.register(r'group', Group1)#组的自定义方法 包含更新权限信息
system_url.register(r'group', GroupViewSet)#组的基本增删改查
system_url.register(r'', GroupPermission)#查询指定id组的权限
system_url.register(r'', TablepermissionView)#查询指定id表的权限，登录用户

from AuthorityManage.views.token import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from AuthorityManage.views.user_group import UserGroup
from AuthorityManage.views.logout import LogoutView
from AuthorityManage.views.tabledirectory import TableView

urlpatterns = [
    # 获取Token的接口
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新Token有效期的接口
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # 验证Token的有效性
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # 登录
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('get_token/', get_token),
    # 登出
    path('logout/', LogoutView.as_view()),
    # 根据用户权限返回表单列表
    path('table/', TableView.as_view()),
    path('user/user_info/', UserViewSet.as_view({'get': 'user_info', 'put': 'update_user_info'})),
    re_path('user/change_password/(?P<pk>.*?)/', UserViewSet.as_view({'put': 'change_password'})),
    path('usergroup/', UserGroup.as_view()),
    re_path('userpermission/(?P<pk>.*?)/', UserPermission.as_view(), name='user_permission'),
    # re_path('grouppermission/(?P<pk>.*?)/', GroupPermission.as_view(), name='user_permission')

]
urlpatterns += system_url.urls
