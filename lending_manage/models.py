from django.db import models
from inbound_manage.models import Inbound

# Create your models here.

"""
表 借测明细
字段 ID 单据外键 借用人 借用日期 借用期限 项目名 产品外键 归还日期 备注 借测类型

表 借测单据
字段 ID 借测表单
"""


class Lending(models.Model):
    borrow_man = models.CharField(max_length=20)
    borrow_date = models.DateField()
    project_name = models.CharField(max_length=50)
    duration = models.CharField(max_length=20)
    return_date = models.DateField()
    comments = models.CharField(max_length=100)
    type = models.CharField(max_length=10)
    borrow_product = models.ForeignKey(to=Inbound, on_delete=models.DO_NOTHING)

    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True


class Receipts(models.Model):
    receipt = models.CharField(max_length=100)
    specify_lending = models.OneToOneField(to=Lending, on_delete=models.DO_NOTHING)
