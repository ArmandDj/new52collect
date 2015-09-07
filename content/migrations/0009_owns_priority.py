# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0008_owns_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='owns',
            name='priority',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
