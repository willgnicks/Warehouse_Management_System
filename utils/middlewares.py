from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from home_login.views import __session_key__, __status_code__
from consumer_manage.models import Consumer


class LoginMiddleware(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__()
        self.get_response = get_response

    @staticmethod
    def process_request(request):
        black_list = ['/consumers/']
        # 如果url在白名单，通过中间件至urls.py
        def is_permitted(path):
            white_list = ['/login/', '/middle/', '/logout/']
            for route in white_list:
                if route.__contains__(path):
                    return True 
            return False
        print('请求路径-->', request.path)              
        if is_permitted(request.path):
            return None
        else:
            request_user = Consumer.objects.filter(name=request.session.get('username')).first()
            
            # 登录session为空，非法登陆返回登陆页面
            if request.session.is_empty():
                print('无session')
                __status_code__['status'] = 1
                return redirect(reverse('home_and_login:go_login'))
            # 单点登陆，如果该用户在其他浏览器或地址登陆，则返回登录页面并显示信息
            elif request.session.session_key != __session_key__.get(request.session.get('username')):
                print('已在其他地方登录')
                print(request.session.session_key)
                print(__session_key__.get(request.session.get('username')))
                __status_code__['status'] = 2
                return redirect(reverse('home_and_login:go_login'))
            elif request_user.type == 2 and request.path in black_list:
                __status_code__['status'] = 3
                print('非法请求')
                request.session.flush()
                return redirect(reverse('home_and_login:go_login'))
            else:
                name = request.session['username']
                print(f'session正常，欢迎{name}')
                return None
