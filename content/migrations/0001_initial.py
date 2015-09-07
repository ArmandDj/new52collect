# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('series', models.TextField()),
                ('issue_num', models.IntegerField()),
                ('title', models.TextField()),
                ('writer', models.TextField()),
                ('penciller', models.TextField()),
                ('rating', models.FloatField()),
                ('cover_price', models.FloatField()),
                ('characters', models.ManyToManyField(to='content.Character')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
