# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-02 17:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zip', '0015_zipusers'),
    ]

    operations = [
        migrations.AddField(
            model_name='ziporder',
            name='order_hidden',
            field=models.BooleanField(default=False),
        ),
    ]
