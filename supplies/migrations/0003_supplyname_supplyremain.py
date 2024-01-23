# Generated by Django 4.2.6 on 2023-11-18 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0002_suppliesgroup_alter_suppliesusers_role_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SupplyRemain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remains', models.IntegerField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplies.suppliesgroup')),
                ('supply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplies.supplyname')),
            ],
        ),
    ]