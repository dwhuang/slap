# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0003_auto_20141201_0141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='slapmaster.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='response',
            name='author',
            field=models.ForeignKey(to='slapmaster.User'),
            preserve_default=True,
        ),
    ]
