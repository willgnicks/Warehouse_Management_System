from django.db import models


# 用户类
class Consumer(models.Model):
    # 用户名
    name = models.CharField(max_length=100, unique=True)
    # 用户密码
    password = models.CharField(max_length=100)
    # 用户联系方式
    phone = models.BigIntegerField(unique=True)
    # 用户性别
    gender = models.SmallIntegerField(choices=[(0,'male'),(1,'female')])
    # 用户邮箱
    mail = models.EmailField(max_length=30, unique=True)
    # 用户状态
    status = models.SmallIntegerField(choices=[(0,'未启用'),(1,'启用中')])
    # 用户类型
    type = models.SmallIntegerField(choices=[(0,'超级管理员'),(1,'管理用户'),(2,'普通用户')])
    # 用户最后登陆日期
    last_login_date = models.DateTimeField(null=True)
    # 存放用户的session key
    # user_session = models.CharField(max_length=40)
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    # 文本用户名
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
