# Generated by Django 3.1.7 on 2021-06-23 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('phone', models.BigIntegerField(unique=True)),
                ('gender', models.CharField(choices=[(0, 'male'), (1, 'female')], max_length=10)),
                ('mail', models.EmailField(max_length=30, unique=True)),
                ('status', models.CharField(choices=[(0, '未启用'), (1, '启用中')], max_length=10)),
                ('type', models.CharField(choices=[(0, '超级管理员'), (1, '管理用户'), (2, '普通用户')], max_length=10)),
                ('last_login_date', models.DateTimeField(null=True)),
                ('flag', models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
