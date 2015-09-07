# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0004_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Owns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.TextField()),
                ('read', models.BooleanField()),
                ('comic', models.ForeignKey(to='content.Comic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
