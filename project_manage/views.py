from django.forms import ModelForm
from project_manage.models import Project
from utils.utils import get_all, put_one, delete_one
from django.shortcuts import redirect, reverse


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['flag']
        error_messages = {
            'project_name': {'required': '请填入项目名称'},
            'project_code': {'required': '请填入项目编号'},
        }


# 添加项目信息
def add_project(request):
    return put_one(request, ProjectForm, kwargs={'reverse_url': 'project_related:all_project_details'})


# 按照默认分页返回详情
def get_all_projects(request):
    return get_all(request=request, klass=Project)


def delete_project(request, pk=1):
    # Project.objects.filter(id=pk).update(flag=False)
    # return redirect(reverse('project_related:all_project_details'))
    return delete_one(pk=pk, klass=Project, kwargs={'reverse_url': 'project_related:all_project_details'})
