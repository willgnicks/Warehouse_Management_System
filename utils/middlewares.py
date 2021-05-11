from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from home_login.views import __session_key__, __status_code__
from user_manage.models import User


class LoginMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__()
        self.get_response = get_response

    @staticmethod
    def process_request(request):
        white_list = ['/', '/login/', '/middle/', '/logout/']
        black_list = ['/users/']
        # 如果url在白名单，通过中间件至urls.py
        if request.path in white_list:
            return None
        else:
            print(request.session.get_expiry_date())
            request_user = User.objects.filter(name=request.session.get('username')).first()
            print(request_user)
            # 登录session为空，非法登陆返回登陆页面
            if request.session.is_empty():
                print('you entered this method because you have no session')
                __status_code__['status'] = 1
                return redirect(reverse('home_and_login:go_login'))
            # 单点登陆，如果该用户在其他浏览器或地址登陆，则返回登录页面并显示信息
            elif request.session.session_key != __session_key__.get(request.session.get('username')):
                print('you entered this method because your account has been used somewhere else')
                print(request.session.session_key)
                print(request.session.get('username'))
                print(__session_key__.get(request.session.get('username')))
                __status_code__['status'] = 2
                return redirect(reverse('home_and_login:go_login'))
            elif request_user.type == '普通用户' and request.path in black_list:
                __status_code__['status'] = 3
                request.session.flush()
                return redirect(reverse('home_and_login:go_login'))
            else:
                name = request.session['username']
                print(f'your session is wonderful, welcome {name}')
                return None
