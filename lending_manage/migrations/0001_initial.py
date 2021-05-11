# Generated by Django 3.1.7 on 2021-05-08 00:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inbound_manage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lending',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_man', models.CharField(max_length=20)),
                ('borrow_date', models.DateField()),
                ('project_name', models.CharField(max_length=50)),
                ('duration', models.CharField(max_length=20)),
                ('return_date', models.DateField()),
                ('comments', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=10)),
                ('flag', models.BooleanField(choices=[(True, '未删除'), (False, '已删除')], default=True)),
                ('borrow_product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inbound_manage.inbound')),
            ],
        ),
        migrations.CreateModel(
            name='Receipts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receipt', models.CharField(max_length=100)),
                ('specify_lending', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='lending_manage.lending')),
            ],
        ),
    ]
