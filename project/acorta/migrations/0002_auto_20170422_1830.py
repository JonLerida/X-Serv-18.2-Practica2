# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acorta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLModel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('larga', models.CharField(max_length=200)),
                ('corta', models.CharField(max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='URL',
        ),
    ]
