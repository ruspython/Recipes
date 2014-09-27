# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_recipe_text_highlighted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='text_highlighted',
        ),
    ]
