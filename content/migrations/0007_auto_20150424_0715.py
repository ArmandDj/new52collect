# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_wish'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='comic',
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
        migrations.AddField(
            model_name='owns',
            name='wish',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='owns',
            name='read',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
