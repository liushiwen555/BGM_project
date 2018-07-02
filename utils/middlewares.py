import logging

from django.conf import settings
from django.http.response import JsonResponse
from django.contrib.auth import logout
import time
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


logger = logging.getLogger(__name__)


class SessionTimeoutMiddleware:
    """
    自动登出无操作的用户
    排除来自本地的用户， 排除带有`MACHINE-PULL`请求头的 request， `MACHINE-PULL`用于前端轮询时携带的请求头。
    对于普通请求， 检测session 中的`last_touch`时间戳和当前时间戳的时间差， 高于 settings 中的INACTIVITY_TIMEOUT设定时间时自动
    登出， 并且返回302状态码， 携带 json 数据， 返回的头部中不携带 location信息。
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.inactivity_timeout = settings.INACTIVITY_TIMEOUT

    def process_view(self, request, view_func, view_args, view_kwargs):
        session = request.session
        machine_pull = request.META.get('HTTP_MACHINE_PULL')
        has_token = request.META.get('HTTP_AUTHORIZATION')
        if not has_token:
            # 对未登录的用户无处理
            return
        if request.META['REMOTE_ADDR'] != '127.0.0.1' and not machine_pull:
            try:
                if time.time() - session['last_touch'] > self.inactivity_timeout:
                    try:
                        # 从 Token 中取出 user
                        auth = TokenAuthentication()
                        user, token = auth.authenticate(request)
                        request.user = user
                        logout(request)
                        return JsonResponse(status=302, data={'info': "长时间无操作自动登出， 请重新登录"})

                    except AuthenticationFailed:
                        # 可能在请求登录接口的时候携带了已经过期的 token
                        return JsonResponse(status=401, data={'info': "Invalid Token."})

            except KeyError:
                pass

            session['last_touch'] = time.time()

    def __call__(self, request):
        response = self.get_response(request)
        return response


class ErrorLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code >= 300 or response.status_code < 200:
            if request.method == 'GET' or request.method == 'DELETE':
                logger.warning("query params :" + request.META['QUERY_STRING'])
            else:
                pass
            logger.error(response.content)

        return response
