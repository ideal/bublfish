# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment_id', models.AutoField(serialize=False, primary_key=True)),
                ('user_id', models.IntegerField(default=0)),
                ('comment_type', models.IntegerField(default=1, verbose_name=b'1: normal comment, 2: reply')),
                ('comment_date', models.DateTimeField(verbose_name=b'date published')),
                ('comment_content', models.TextField(max_length=4096)),
                ('comment_ups', models.IntegerField(default=0)),
                ('comment_downs', models.IntegerField(default=0)),
                ('comment_parent', models.BigIntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
