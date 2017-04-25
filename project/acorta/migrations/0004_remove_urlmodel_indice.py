# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0003_urlmodel_indice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='urlmodel',
            name='indice',
        ),
    ]
