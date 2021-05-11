from django.db import models
from purchase_manage.models import Purchase


# Create your models here.


class Inbound(models.Model):
    material_code = models.CharField(max_length=30)
    purchase_belong = models.ForeignKey(to=Purchase, on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField()
    equipment_ID = models.CharField(max_length=40)
    in_house_date = models.DateField()
    status = models.CharField(max_length=30)
    comments = models.CharField(max_length=50)
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True

    class Meta:
        ordering = ['material_code']


class Receipts(models.Model):
    receipt = models.BinaryField(bytes)
    specific_inbound = models.ForeignKey(to=Inbound, on_delete=models.DO_NOTHING)
