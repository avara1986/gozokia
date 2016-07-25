# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-25 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djgozokia', '0002_auto_20160725_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gozokiachat',
            name='rule',
            field=models.CharField(blank=True, choices=[('O', 'Gozokia'), ('I', 'User')], max_length=70, null=True),
        ),
        migrations.AlterField(
            model_name='gozokiachat',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='gozokiachat',
            name='type_rule',
            field=models.CharField(blank=True, choices=[('O', 'Gozokia'), ('I', 'User')], max_length=2, null=True),
        ),
    ]