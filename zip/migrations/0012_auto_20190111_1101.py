# Generated by Django 2.1.5 on 2019-01-11 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zip', '0011_auto_20190111_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='ziporder',
            name='order_closed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ziporder',
            name='order_temp',
            field=models.BooleanField(default=True),
        ),
    ]
