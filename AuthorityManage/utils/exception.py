# -*- coding: utf-8 -*-

import logging
import traceback

from django.db.models import ProtectedError
from rest_framework import exceptions
from rest_framework.exceptions import APIException as DRFAPIException, AuthenticationFailed
from rest_framework.views import set_rollback

from AuthorityManage.utils.json_response import ErrorResponse

logger = logging.getLogger(__name__)


def CustomExceptionHandler(ex, context):
    """
    统一异常拦截处理
    目的:(1)取消所有的500异常响应,统一响应为标准错误返回
        (2)准确显示错误信息
    :param ex:
    :param context:
    :return:
    """
    message = ''
    code = 400

    if isinstance(ex, AuthenticationFailed):
        code = 401
        message = ex.detail
    elif isinstance(ex, DRFAPIException):
        set_rollback()
        message = ex.detail
    elif isinstance(ex, exceptions.APIException):
        set_rollback()
        message = ex.detail
    elif isinstance(ex, ProtectedError):
        set_rollback()
        message = "删除失败:该条数据与其他数据有相关绑定"
    # elif isinstance(ex, DatabaseError):
    #     set_rollback()
    #     message = "接口服务器异常,请联系管理员"
    elif isinstance(ex, Exception):
        logger.error(traceback.format_exc())
        message = str(ex)

    # errorMsg = message
    # for key in errorMsg:
    #     message = errorMsg[key][0]

    return ErrorResponse(message=message, code=code)
