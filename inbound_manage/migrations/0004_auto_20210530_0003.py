# Generated by Django 3.1.7 on 2021-05-30 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inbound_manage', '0003_auto_20210529_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbound',
            name='in_house_date',
            field=models.DateField(auto_now=True),
        ),
    ]
