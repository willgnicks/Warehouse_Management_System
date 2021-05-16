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
    gender = models.CharField(max_length=10)
    # 用户邮箱
    mail = models.EmailField(max_length=30, unique=True)
    # 用户状态
    status = models.CharField(max_length=10)
    # 用户类型
    type = models.CharField(max_length=10)
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
