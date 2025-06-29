from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    """ 中间件1 """
    def process_request(self, request):
        # 0.排除不需要登录的页面
        # 获取当前用户请求的url /login/
        if request.path_info in ["/login/", "/image/code/"]:
            return None
        # 1、先获取浏览器中的session信息是否存在
        info_dict = request.session.get('info')
        if info_dict:
            print("中间件收到的是：")
            print(info_dict)
            return None
        return redirect('/login/')

