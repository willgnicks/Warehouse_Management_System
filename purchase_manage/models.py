from django.db import models
from project_manage.models import Project


# Create your models here.
class Purchase(models.Model):
    form_number = models.CharField(max_length=30, unique=True)
    contract_number = models.CharField(max_length=30, unique=True)
    demand_person = models.CharField(max_length=10)
    handle_man = models.CharField(max_length=10)
    purchase_date = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(to=Project, null=True, on_delete=models.DO_NOTHING)
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)
    inbound_flag = models.BooleanField(choices=[(True, '已入库'), (False, '未入库')], default=False)

    def __isClosed__(self):
        return self.flag

    class Meta:
        ordering = ['id']


class Receipts(models.Model):
    receipt = models.CharField(max_length=100)
    specify_purchase = models.ForeignKey(to=Purchase, on_delete=models.DO_NOTHING)
