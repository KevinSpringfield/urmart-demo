# Generated by Django 2.2.4 on 2019-08-09 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backstage', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_id',
            field=models.IntegerField(default=0, verbose_name='顧客ID'),
            preserve_default=False,
        ),
    ]