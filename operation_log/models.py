from django.db import models
from consumer_manage.models import Consumer


# Create your models here.
# 操作日志详情
class LogDetail(models.Model):
    # 之前的数据库数据
    previous_data = models.JSONField()
    # 之后的数据库数据
    posterior_data = models.JSONField()


class LogSummary(models.Model):
    type = [(1, '登陆'), (2, '新增'), (3, '修改'), (4, '删除')]
    # 登陆的用户
    consumer_id = models.ForeignKey(to=Consumer, related_name="Log_related_consumer", on_delete=models.DO_NOTHING)
    # 用户IP
    log_ip = models.CharField(max_length=30)
    # 登陆时间
    log_date = models.DateField()
    # 操作类型
    operation_type = models.SmallIntegerField(choices=type)
    # 详细数据关联
    log_details = models.ForeignKey(to=LogDetail, related_name="Details_of_operation", on_delete=models.DO_NOTHING)
