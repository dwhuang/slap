# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0005_auto_20141204_0051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='vote',
            new_name='upvote',
        ),
    ]
