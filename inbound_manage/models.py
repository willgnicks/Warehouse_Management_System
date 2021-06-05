from django.db import models
from product_manage.models import PurchaseProductRel


# Create your models here.


class Inbound(models.Model):
    material_code = models.CharField(max_length=30, unique=True)
    in_house_date = models.DateField(auto_now=True)
    pp_rel = models.ForeignKey(to=PurchaseProductRel, on_delete=models.DO_NOTHING)
    comments = models.CharField(max_length=50)
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)

    def __close__(self):
        self.flag = True
        return True

    class Meta:
        ordering = ['id']


class Receipts(models.Model):
    receipt = models.BinaryField(bytes)
    specific_inbound = models.ForeignKey(to=Inbound, on_delete=models.DO_NOTHING)
