# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-30 14:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FOSS_Analysis', '0002_auto_20160530_1024'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='blame',
            unique_together=set([('file', 'author')]),
        ),
    ]
