# Generated by Django 3.1.7 on 2021-06-23 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consumer_manage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumer',
            name='gender',
            field=models.SmallIntegerField(choices=[(0, 'male'), (1, 'female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未启用'), (1, '启用中')], max_length=10),
        ),
        migrations.AlterField(
            model_name='consumer',
            name='type',
            field=models.SmallIntegerField(choices=[(0, '超级管理员'), (1, '管理用户'), (2, '普通用户')], max_length=10),
        ),
    ]