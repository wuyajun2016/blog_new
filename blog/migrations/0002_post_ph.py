# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-16 14:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='ph',
            field=models.ImageField(default=1, upload_to='uploadImages', verbose_name='图片'),
            preserve_default=False,
        ),
    ]
