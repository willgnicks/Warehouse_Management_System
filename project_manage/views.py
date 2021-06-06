from django.forms import ModelForm
from project_manage.models import Project
from utils.utils import get_all, add_or_update, delete_one, get_one
from django.shortcuts import redirect, reverse, render


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['flag', 'project_status']
        error_messages = {
            'project_name': {'required': '请填入项目名称',
                             'unique': '该项目名已经存在'},

            'project_code': {'required': '请填入项目编号',
                             'unique': '该项目编号已经存在'},
        }


def get_one_project(request, pk):
    return get_one(request, Project, kwargs={'pk': pk})


# 添加项目信息
def add_project(request):
    return add_or_update(request, Project, ProjectForm,
                         kwargs={'reverse_url': 'project_related:all_project_details'})


# 按照默认分页返回详情
def get_all_projects(request):
    return get_all(request=request, klass=Project)


def get_query_projects(request):
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'project_name__icontains': query_data,
              'project_code__icontains': query_data} if query_data is not None else {}
    return get_all(request, Project, kwargs={'query': kwargs})


def delete_project(request, pk=1):
    return delete_one(pk=pk, klass=Project, kwargs={'reverse_url': 'project_related:all_project_details'})
