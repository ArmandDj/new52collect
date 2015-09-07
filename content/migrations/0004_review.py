# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_auto_20150417_0757'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.TextField()),
                ('content', models.TextField()),
                ('date', models.DateField()),
                ('comic', models.ForeignKey(to='content.Comic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
