# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='cover',
            field=models.ImageField(null=True, upload_to=b''),
            preserve_default=True,
        ),
    ]
