# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0002_auto_20170423_0206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='nickname',
            field=models.CharField(default=b'\xe4\xb8\x8d\xe9\xa1\x98\xe6\x84\x8f\xe9\x80\x8f\xe6\xbc\x8f\xe8\xba\xab\xe4\xbb\xbd\xe7\x9a\x84\xe4\xba\xba', max_length=10),
        ),
    ]
