# Generated by Django 3.1.7 on 2021-06-23 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_code', models.CharField(max_length=30, unique=True)),
                ('in_house_date', models.DateField(auto_now=True)),
                ('comments', models.CharField(max_length=50)),
                ('flag', models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)),
                ('pp_rel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product_manage.purchaseproductrel')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.BinaryField(verbose_name=bytes)),
                ('specific_inbound', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inbound_manage.inbound')),
            ],
        ),
    ]
