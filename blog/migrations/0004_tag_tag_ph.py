# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-17 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='tag_ph',
            field=models.ImageField(default=1, upload_to='uploadImages', verbose_name='类目图'),
            preserve_default=False,
        ),
    ]
