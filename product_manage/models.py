from django.db import models
from user_manage.models import User
from manufacturer_manage.models import Manufacturer
from purchase_manage.models import Purchase


# 产品模型
class Product(models.Model):
    # 产品名称
    product_name = models.CharField(max_length=30)
    # 产品型号
    product_model = models.CharField(max_length=100)
    # 产品类型
    product_type = models.CharField(max_length=100)
    # 产品单价
    unit_price = models.IntegerField()
    # 制造商
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING, related_name='company_made_it')
    # 删除
    flag = models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)
    # 与采购多对多
    purchase = models.ManyToManyField(to=Purchase, through='PurchaseProductRel')

    def __close__(self):
        self.flag = True
        return True

    # 文本产品名
    def __str__(self):
        return self.product_name

    class Meta:
        ordering = ['product_name']


class PurchaseProductRel(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.SmallIntegerField()

    class Meta:
        ordering = ['id']

# # 产品-用户关系表
# class ProductUserRelationship(models.Model):
#     # 产品
#     product_foreignKey = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
#     # 录入时间
#     register_date = models.DateField()
#     # 录入人
#     register_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='add_user')
#     # 修改时间
#     amend_date = models.DateField()
#     # 修改人
#     amend_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='amend_user')
#     # 删除时间
#     delete_date = models.DateField()
#     # 删除人
#     delete_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='delete_user')
#
#     def __str__(self):
#         return self.register_date


# # 供应商-用户关系表
# class ManufacturerUserRelationship(models.Model):
#     # 供应商
#     manufacturer_foreignKey = models.ForeignKey(Manufacturer, on_delete=models.DO_NOTHING)
#     # 录入时间
#     register_date = models.DateField()
#     # 录入人
#     register_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='add_manufacturer_user')
#     # 修改时间
#     amend_date = models.DateField()
#     # 修改人
#     amend_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='amend_manufacturer_user')
#     # 删除时间
#     delete_date = models.DateField()
#     # 删除人
#     delete_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='delete_manufacturer_user')
#
#     def __str__(self):
#         return self.register_date
