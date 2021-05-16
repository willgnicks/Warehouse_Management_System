from django.db import models


# 项目管理
class Project(models.Model):
    # 项目名
    project_name = models.CharField(max_length=30, unique=True)
    # 项目编号
    project_code = models.CharField(max_length=30, unique=True)
    # 用来删除项目，实际数据库不删除，展示删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    class Meta:
        ordering = ['project_code']

    # 文本项目名
    def __str__(self):
        return self.project_name

