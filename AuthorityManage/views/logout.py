from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from AuthorityManage.utils.json_response import SuccessResponse, ErrorResponse

class LogoutView(APIView):
    """
    登出接口
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 退出登录
        logout(request)
        # # 清除cookier
        # response = redirect('/api-auth/login/?next=/swagger/')
        # response.delete_cookie('username')
        return SuccessResponse()
