# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_comic_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comic',
            name='cover',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
