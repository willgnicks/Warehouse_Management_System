import time
from datetime import datetime
import string
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse


def get_model_name(klass):
    return klass.__name__.lower() + 's'


def get_model_name_from_modelform(klass):
    return klass.__name__.lower()[:-4] + 's'


def get_all(request, klass, **kwargs):
    """
    :param request:
    :param klass: 传入检索的类名
    :param kwargs: 传入同model类的类名全小写加s，生成html的路径，并且生成用来生成字典的key方便html渲染
    :return:
    """
    # 获取实参类的类名
    class_name = get_model_name(klass=klass)
    # 生成分页器
    print(time.time())
    # paginator = {}
    # if class_name == 'users':
    #     paginator = Paginator(klass.objects.all(), 10)
    # else:
    paginator = Paginator(klass.objects.all().filter(flag=True), 10)
    # get方法的html路径

    template_url = f'{class_name}/{class_name}.html'
    print(class_name, '&', template_url)
    if request.GET.get('page') is None:
        query_data = paginator.page(1)
        print(time.time())
    else:
        query_data = paginator.page(request.GET.get('page'))
    return render(request,
                  template_url,
                  {class_name: query_data, 'count': paginator.count}
                  )


def put_one(request, form_class, **kwargs):
    """
    :param request:
    :param form_class: 传入添加的modelform类名
    :param kwargs: 其中参数：key=['quote_class', 'reverse_url']
    :return:
    """
    # 获取表单类中的模型类名
    model_name = get_model_name_from_modelform(form_class)
    # put方法的html路径
    template_url = f'{model_name}/add.html'
    # modelform表单实力化
    modelform_instance = form_class(request.POST)
    # 初始化返回字典
    return_dic = {model_name: modelform_instance}
    # 获取引用类list, 无值传空
    quote_class_list = kwargs.get('kwargs').get('quote_class')
    quote_dic = {}
    if quote_class_list is not None:
        for klass in quote_class_list:
            quote_dic[get_model_name(klass)] = klass.objects.all()
    print(model_name, '&', template_url)
    if request.method == 'GET':
        return render(request, template_url, quote_dic)
    else:
        if modelform_instance.is_valid():
            modelform_instance.save()
            return HttpResponseRedirect(
                reverse(
                    kwargs.get('kwargs').get('reverse_url')
                )
            )
        else:
            for key in quote_dic:
                return_dic[key] = quote_dic.get(key)
            return render(request, template_url, return_dic)


def delete_one(pk, klass, **kwargs):
    klass.objects.filter(id=pk).update(flag=False)
    return HttpResponseRedirect(
        reverse(
            kwargs.get('kwargs').get('reverse_url')))


"""

    def is_user_login(request):
        return False if request.session.is_empty() else True


    def is_user_login_somewhere_else(request):
        return False if request.session.session_key == User.objects.filter(
            name=request.session.get('username')).first().user_session else True


    def return_to_login_with_message(request, message):
        return HttpResponseRedirect(reverse('home_and_login:go_login', kwargs={'message': message}))


    def is_request_valid(request):
        if is_user_login(request) is False:
            return return_to_login_with_message(request, '您还没有登陆')
        elif is_user_login_somewhere_else(request) is True:
            return return_to_login_with_message(request, '您的账户已在其他地方登陆，如不是本人操作，请及时联系管理员修改密码')
"""
