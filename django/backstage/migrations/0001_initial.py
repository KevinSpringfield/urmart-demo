# Generated by Django 2.2.4 on 2019-08-07 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(verbose_name='商品ID')),
                ('qty', models.IntegerField(default=0, verbose_name='購買數量')),
                ('price', models.IntegerField(default=0, verbose_name='商品單價')),
                ('shop_id', models.CharField(max_length=2, verbose_name='商品所屬館別')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_id', models.IntegerField(unique=True, verbose_name='商品ID')),
                ('stock_pcs', models.IntegerField(default=0, verbose_name='商品庫存數量')),
                ('price', models.IntegerField(default=0, verbose_name='商品單價')),
                ('shop_id', models.CharField(choices=[('um', 'um'), ('ms', 'ms'), ('ps', 'ps')], max_length=2, verbose_name='商品所屬館別')),
                ('vip', models.BooleanField(default=False, verbose_name='VIP限定商品')),
            ],
        ),
    ]