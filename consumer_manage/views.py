from django.shortcuts import render, redirect, reverse
from django.forms import ModelForm
from consumer_manage.models import Consumer
from utils.utils import get_all, add_or_update, get_one, delete_one


# Create your views here.
class ConsumerForm(ModelForm):
    class Meta:
        model = Consumer
        fields = '__all__'
        exclude = ['last_login_date', 'flag']
        error_messages = {
            'name': {'required': '请输入用户名', 'unique': '该用户名已注册', 'max_length': '用户名长度不得超过10'},
            'password': {'required': '请输入用户密码', 'max_length': '用户密码长度不得超过10'},
            'mail': {'required': '请输入邮箱', 'unique': '该邮箱已注册'},
            'phone': {'required': '请输入手机号码', 'unique': '该手机号码已注册', 'invalid': '请输入正确的手机号码'},
            'status': {'required': '请选择用户状态', 'max_length': '用户名长度不得超过10'},
            'type': {'required': '请选择用户类型', 'max_length': '用户名长度不得超过10'},
            'gender': {'required': '请选择用户性别', 'max_length': '用户名长度不得超过10'},

        }


def get_all_consumers(request):
    return get_all(request=request, klass=Consumer)


def add_consumer(request):
    return add_or_update(request=request, klass=Consumer, form_class=ConsumerForm,
                         kwargs={'reverse_url': 'consumer_related:all_consumers_details'})


def delete_consumer(request, pk):
    return delete_one(pk=pk, klass=Consumer, kwargs={'reverse_url': 'consumer_related:all_consumers_details'})


def get_one_consumer(request, pk):
    return get_one(request, Consumer, kwargs={'pk': pk})


def get_query_consumers(request):
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'name__icontains': query_data,
              'phone__icontains': query_data} if query_data is not None else {}
    return get_all(request, Consumer, kwargs={'query': kwargs})
