# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='text_highlighted',
            field=models.TextField(default='', blank=True, editable=False),
            preserve_default=False,
        ),
    ]
