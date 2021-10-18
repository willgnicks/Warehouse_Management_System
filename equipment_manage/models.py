from django.db import models
from inbound_manage.models import Inbound
from outbound_manage.models import Outbound
from reception_manage.models import Reception


class Equipment(models.Model):
    inbound = models.ForeignKey(Inbound, on_delete=models.DO_NOTHING)
    outbound = models.ForeignKey(Outbound, null=True, on_delete=models.DO_NOTHING)
    reception = models.ForeignKey(Reception, null=True, on_delete=models.DO_NOTHING)
    SN = models.CharField(max_length=200, unique=True)
    status_code = models.SmallIntegerField(choices=[(0, '在库'), (1, '出库'), (2, '外借'), (3, '内借'), (4, '领用')], default=0)
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    # 设备SN
    def __str__(self):
        return self.SN

    class Meta:
        ordering = ['id']
