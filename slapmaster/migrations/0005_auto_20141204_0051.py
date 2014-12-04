# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0004_auto_20141201_0141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fb_link',
            new_name='show_fb_url',
        ),
    ]
