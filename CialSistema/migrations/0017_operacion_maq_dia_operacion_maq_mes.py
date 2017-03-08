# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 12:45
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CialSistema', '0016_auto_20170223_1636'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operacion_maq_dia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=20)),
                ('Modelo', models.CharField(max_length=50)),
                ('patente', models.CharField(max_length=50)),
                ('mes', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Operacion_maq_mes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora', models.DecimalField(decimal_places=1, default=Decimal('0.0'), max_digits=20)),
                ('Modelo', models.CharField(max_length=50)),
                ('patente', models.CharField(max_length=50)),
                ('mes', models.CharField(max_length=50)),
            ],
        ),
    ]