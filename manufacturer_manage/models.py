from django.db import models
from datetime import datetime


# Create your models here.

# 供应商模型
class Manufacturer(models.Model):
    # 供应商名
    manufacturer_name = models.CharField(max_length=50)
    # 联系人
    manufacturer_linkman = models.CharField(max_length=20)
    # 联系方式
    manufacturer_contact = models.CharField(max_length=20)
    # 开始合作日期
    cooperation_begin_date = models.DateField()
    # 合作状态枚举
    cooperation_status = [(True, '合作中'), (False, '未合作')]
    # 是否合作
    is_cooperated = models.BooleanField(choices=cooperation_status, default=True)
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True

    # 文本供应商名
    def __str__(self):
        return self.manufacturer_name

    class Meta:
        ordering = ['is_cooperated']
