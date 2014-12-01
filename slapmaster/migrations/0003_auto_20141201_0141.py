# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0002_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(default=1, to='slapmaster.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response',
            name='author',
            field=models.ForeignKey(default=1, to='slapmaster.User'),
            preserve_default=True,
        ),
    ]
