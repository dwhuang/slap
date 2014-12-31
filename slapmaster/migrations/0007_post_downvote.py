# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0006_auto_20141230_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='downvote',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]
