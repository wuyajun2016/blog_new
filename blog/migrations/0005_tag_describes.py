# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-07-17 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_tag_tag_ph'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='describes',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
