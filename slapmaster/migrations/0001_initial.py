# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('news_url', models.URLField(max_length=1024)),
                ('reason', models.CharField(max_length=1024)),
                ('vote', models.PositiveIntegerField(default=0)),
                ('views', models.PositiveIntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('response_text', models.TextField()),
                ('upvote', models.PositiveIntegerField(default=0)),
                ('downvote', models.PositiveIntegerField(default=0)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('original_post', models.ForeignKey(to='slapmaster.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
