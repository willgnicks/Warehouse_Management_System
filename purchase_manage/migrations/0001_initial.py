# Generated by Django 3.1.7 on 2021-05-08 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_number', models.CharField(max_length=30, unique=True)),
                ('contract_number', models.CharField(max_length=30, unique=True)),
                ('demand_person', models.CharField(max_length=10)),
                ('handle_man', models.CharField(max_length=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('flag', models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='project_manage.project')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.CharField(max_length=100)),
                ('specify_purchase', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='purchase_manage.purchase')),
            ],
        ),
    ]
