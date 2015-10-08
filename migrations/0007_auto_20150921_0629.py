# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='threads',
            field=models.ManyToManyField(to='blog.Comment', blank=True),
            preserve_default=True,
        ),
    ]
