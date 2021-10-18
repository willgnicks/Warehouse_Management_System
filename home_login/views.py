from django import forms
from django.shortcuts import render, HttpResponseRedirect
from consumer_manage.models import Consumer
from django.http import HttpResponse
import json
from django.forms import Form, fields
from django.urls import reverse
from datetime import date, datetime


class LoginForm(Form):
    username = fields.CharField(required=True,
                                error_messages={'required': '用户名不能为空'})
    password = fields.CharField(required=True,
                                error_messages={'required': '用户密码不能为空'})


__session_key__ = {}
__status_code__ = {'status': 0}

def login(request):
    """

    :param request:
    __status_code__: 状态参数，中间件传值，
                   状态 1： int参数 1，用户未登陆
                   状态 2： int参数 2，用户账号于其他地方登陆
                   状态 3： 无参数，账户正常
    __session_key__: 记录用户的session_key，用来验证单点登陆

    1、第一次登录时，通过中间件白名单，到达该view方法，此时status_code为零，不展示任何错误信息。
    2、遇任何非法登陆，中间件拦截验证用户无session，更改状态码为1，重定向至该方法，强制返回登录页面并携带错误信息，随后改状态码为0
    3、遇任何非单点登陆情况，__session_key__中记录的最新登录用户的session_key，那么旧登录用户的session_key与__session_key__中记录的最新key值不符，
       那么就用户访问任意网页时中间件将更改状态码为2，重定向至该方法，该方法将强制返回登录页面并携带错误信息，随后更改状态码为0
    4、理念是任何URL的访问必须通过此view方法验证登录后才能正常使用，中间验证件将拦截验证所有URL，访问网站必须通过此通道。
       一、 验证正确的用户信息，更新__session_key__中session_key为最新的用户登录key
       二、 否则随后任意访问中间件将进行拦截验证，验证不通过触发状态码更改，跳转回登录页面
    5、每次修改状态码为0是为防止其他登录用户依旧显示旧状态码报错信息
    6、每次退出时清空用户的session，同浏览器再次登录用户将不携带任何session_key
    :return:
    """
    print(request.method)
    if request.method == 'GET':
        status_code = __status_code__.get('status')
        msg = {}
        if status_code == 1:
            __status_code__['status'] = 0
            msg['msg']='您还没有登录，请先登录'
        elif status_code == 2:
            remote_IP = request.META.get('REMOTE_ADDR')
            msg['msg']=f'您的账号已于{remote_IP}登录'
            __status_code__['status'] = 0
        elif status_code == 3:
            msg['msg']='非法请求，无法访问资源'
            __status_code__['status'] = 0
        return render(request, 'login_home/login.html', msg)    
    else:
        login_form = LoginForm(request.POST)
        return_dict = {'login': login_form}
        # 通过验证
        if login_form.is_valid():
            # 获取该用户信息
            login_user = Consumer.objects.filter(name__exact=login_form.cleaned_data.get('username'))
            user_instance = login_user.first()
            # 该用户存在并且密码通过核对正确
            if login_user.exists() and login_form.cleaned_data.get('password') == user_instance.password:
                # 该用户状态是启用状态
                if user_instance.status == 1:
                    print(request.session.session_key)
                    request.session['username'] = user_instance.name
                    request.session['type'] = user_instance.type
                    # print(request.META)
                    Consumer.objects.filter(name__exact=user_instance.name).update(last_login_date=datetime.now())
                    # 先重定向到中间件生成session
                    return HttpResponseRedirect(reverse('home_and_login:before_go_home'))
                else:
                    return_dict['msg'] = '您的账户已经停用，请联系管理员开启'
            # 用户名或密码不对
            else:
                return_dict['msg'] = '用户名或密码错误'
        # 验证没通过
        return render(request, 'login_home/login.html', return_dict)


# 这是最终显示index页面的view
def go_home(request):
    return render(request, 'login_home/home.html')


def is_user_login(request):
    return False if request.session.is_empty() else True


# 中间session生成函数
def before_go_home(request):
    # 每次登录时先更新session_key的值
    global __session_key__
    __session_key__[request.session.get('username')] = request.session.session_key
    # 然后重定向给主页view
    return HttpResponseRedirect(reverse('home_and_login:go_home'))


def logout(request):
    # 清除此用户的session
    request.session.flush()
    return HttpResponseRedirect(reverse('home_and_login:go_login'))


def valid(request):
    obj = LoginForm(request.POST)
    if obj.is_valid():
        print(obj.cleaned_data)
        dic = {'status': 'true'}
        return HttpResponse(json.dumps(dic))
    else:
        print(obj.errors)
        return HttpResponse({'status': 'false', 'msg': obj.errors})
        # return HttpResponse(v)
