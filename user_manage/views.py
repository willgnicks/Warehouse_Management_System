from django.shortcuts import render, redirect, reverse
from django.forms import ModelForm
from user_manage.models import User
from utils.utils import get_all, put_one


# Create your views here.
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ['last_login_date', 'flag']
        error_messages = {
            'name': {'required': '请输入用户名', 'unique': '该用户名已注册'},
            'password': {'required': '请输入用户密码', 'max_length': '用户名长度不得超过10'},
            'mail': {'required': '请输入邮箱', 'unique': '该邮箱已注册'},
            'phone': {'required': '请输入手机号码', 'unique': '该手机号码已注册', 'invalid': '请输入正确的手机号码'},
            'status': {'required': '请选择用户状态', 'max_length': '用户名长度不得超过10'},
            'type': {'required': '请选择用户类型', 'max_length': '用户名长度不得超过10'},
            'gender': {'required': '请选择用户性别', 'max_length': '用户名长度不得超过10'},

        }


# 返回所有用户
# @login_required(login_url='/login/')
def get_all_users(request):
    return get_all(request, User)


# @login_required(login_url='/login/')
def add_user(request):
    return put_one(request=request, form_class=UserForm, kwargs={'reverse_url': 'user_related:all_users_details'})


def delete_user(request, pk=1):
    User.objects.filter(id=pk).update(flag=False)
    return redirect(reverse('user_related:all_users_details'))

# form验证
# name = fields.CharField(required=True,
#                         max_length=10,
#                         min_length=2,
#                         error_messages={'required': '请输入用户名',
#                                         'max_length': '用户名长度不得超过10',
#                                         'min_length': '用户名长度不得小于2'})
# gender = fields.CharField(required=True,
#                           error_messages={'required': '请选择用户性别'})
# mail = fields.EmailField(error_messages={'required': '请输入邮箱',
#                                          'invalid': '请输入正确的邮箱格式'})
# phone = fields.IntegerField(required=True,
#                             error_messages={'required': '请输入电话',
#                                             'invalid': '请输入正确的电话号码'})
# password = fields.CharField(required=True,
#                             max_length=16,
#                             min_length=8,
#                             error_messages={'required': '请输入用户密码',
#                                             'max_length': '用户密码长度不得超过16',
#                                             'min_length': '用户密码长度不得小于8'})
# type = fields.CharField(required=True,
#                         error_messages={'required': '请选择用户类型'})
# status = fields.CharField(required=True,
#                           error_messages={'required': '请选择用户性别'})
