from django.db import models
from project_manage.models import Project
from inbound_manage.models import Inbound


# Create your models here.


class Outbound(models.Model):
    # 项目管理外键
    project = models.ForeignKey(to=Project, on_delete=models.DO_NOTHING)
    # 入库详情外键
    inbound = models.ForeignKey(to=Inbound, on_delete=models.DO_NOTHING)
    # 出库单据外键
    demand_person = models.CharField(max_length=20)
    outbound_date = models.DateField(auto_now=True)
    contract_number = models.CharField(max_length=50, unique=True)
    form_number = models.CharField(max_length=50, unique=True)
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True

    class Meta:
        ordering = ['outbound_date']


class Receipts(models.Model):
    outbound_receipt = models.BinaryField()
    specific_outbound = models.ForeignKey(to=Outbound, on_delete=models.DO_NOTHING)
