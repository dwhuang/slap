# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slapmaster', '0007_post_downvote'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('power', models.SmallIntegerField()),
                ('post', models.ForeignKey(to='slapmaster.Post')),
                ('user', models.ForeignKey(to='slapmaster.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='voted_post',
            field=models.ManyToManyField(related_name='voter_set', through='slapmaster.PostVote', to='slapmaster.Post'),
            preserve_default=True,
        ),
    ]
