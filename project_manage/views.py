from django.forms import ModelForm
from project_manage.models import Project
from utils.utils import get_all, add_or_update, delete_one
from django.shortcuts import redirect, reverse, render


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['flag']
        error_messages = {
            'project_name': {'required': '请填入项目名称',
                             'unique': '该项目名已经存在'},

            'project_code': {'required': '请填入项目编号',
                             'unique': '该项目编号已经存在'},
        }


def get_one_project(request, pk):
    from utils.utils import get_one
    return get_one(request, Project, kwargs={'pk': pk, 'title': '修改项目详情'})


# 添加项目信息
def add_project(request):
    """

    @param request:
    @return:
    """
    return add_or_update(request, Project, ProjectForm,
                         kwargs={'reverse_url': 'project_related:all_project_details', 'title': '新增项目'})


# 按照默认分页返回详情
def get_all_projects(request):
    """

    @param request:
    @return:
    """
    return get_all(request=request, klass=Project)


def get_query_projects(request):
    query_data = request.GET.get('query') if request.GET.get('query') is not None else None
    kwargs = {'project_name__icontains': query_data,
              'project_code__icontains': query_data} if query_data is not None else {}
    return get_all(request, Project, kwargs={'query': kwargs})


def delete_project(request, pk=1):
    return delete_one(pk=pk, klass=Project, kwargs={'reverse_url': 'project_related:all_project_details'})
