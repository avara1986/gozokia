# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-25 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djgozokia', '0003_auto_20160725_1151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gozokiachat',
            options={'ordering': ('timestamp',), 'verbose_name': 'Gozokia Chat', 'verbose_name_plural': 'Gozokia Chats'},
        ),
        migrations.AlterField(
            model_name='gozokiachat',
            name='status',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]