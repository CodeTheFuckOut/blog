# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20150921_0629'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_child',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
