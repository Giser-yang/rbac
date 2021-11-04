# -*- coding: utf-8 -*-

from rest_framework.response import Response


class SuccessResponse(Response):
    """
    标准响应成功的返回, SuccessResponse(data)或者SuccessResponse(data=data)
    (1)默认code返回2000, 不支持指定其他返回码
    """

    def __init__(self, data=None, message='success', status=None, template_name=None, headers=None, exception=False,
                 content_type=None):
        std_data = {
            "code": 200,
            "data": {
                "page": 1,
                "limit": 1,
                "total": 1,
                "data": data
            },
            "message": message
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)


class ErrorResponse(Response):
    """
    标准响应错误的返回,ErrorResponse(msg='xxx')
    (1)默认错误码返回400, 也可以指定其他返回码:ErrorResponse(code=xxx)
    """

    def __init__(self, data=None, message='error', code=400, status=None, template_name=None, headers=None,
                 exception=False, content_type=None):
        std_data = {
            "code": code,
            "data": data,
            "message": message
        }
        super().__init__(std_data, status, template_name, headers, exception, content_type)
