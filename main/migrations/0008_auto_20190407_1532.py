# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-04-07 06:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20190407_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_post',
            name='photo',
            field=models.ImageField(default='images/post_default.jpg', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='company',
            name='status',
            field=models.CharField(default='company', max_length=10),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(default='profile', max_length=10),
        ),
    ]
