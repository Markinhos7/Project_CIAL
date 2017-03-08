# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 21:12
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CialSistema', '0011_auto_20170222_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquina',
            name='hora',
            field=models.DecimalField(decimal_places=1, default=Decimal('0.00'), max_digits=20),
        ),
    ]