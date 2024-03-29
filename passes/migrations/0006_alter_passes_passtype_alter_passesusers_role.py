# Generated by Django 4.2.6 on 2023-10-20 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passes', '0005_passesemails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='passes',
            name='passtype',
            field=models.CharField(choices=[('afl', 'Пропуск АФЛ'), ('mash', 'Пропуск МАШ')], max_length=10),
        ),
        migrations.AlterField(
            model_name='passesusers',
            name='role',
            field=models.CharField(choices=[('teamlead', 'Руководитель группы'), ('controller', 'Контролер'), ('admin', 'Администратор')], max_length=100),
        ),
    ]
