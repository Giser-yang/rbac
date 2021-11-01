from django.urls import path, re_path
from rest_framework import routers
system_url = routers.SimpleRouter()

from AuthorityManage.system.img_list import ImgViewSet
from AuthorityManage.system.user import UsersViewSet


system_url.register(r'img', ImgViewSet)
system_url.register(r'user', UsersViewSet)


from AuthorityManage.views import ProjectUser
urlpatterns = [
    path(r'project', ProjectUser.as_view()),
]
urlpatterns += system_url.urls
