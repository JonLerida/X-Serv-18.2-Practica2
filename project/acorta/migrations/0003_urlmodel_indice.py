# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0002_auto_20170422_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='urlmodel',
            name='indice',
            field=models.IntegerField(default=0),
        ),
    ]
