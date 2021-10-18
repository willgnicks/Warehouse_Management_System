from django.db import models
from project_manage.models import Project
from inbound_manage.models import Inbound


# Create your models here.


class Outbound(models.Model):
    project = models.ForeignKey(to=Project, on_delete=models.DO_NOTHING)  # 项目关联
    demand_person = models.CharField(max_length=20)  # 需求人
    outbound_date = models.DateField(auto_now=True)  # 出库日期，默认生成日期
    contract_number = models.CharField(max_length=50, unique=True)  # 合同号
    form_number = models.CharField(max_length=50, unique=True)  # 表单号
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True

    class Meta:
        ordering = ['id']


class Receipts(models.Model):
    outbound_receipt = models.BinaryField()
    specific_outbound = models.ForeignKey(to=Outbound, on_delete=models.DO_NOTHING)
