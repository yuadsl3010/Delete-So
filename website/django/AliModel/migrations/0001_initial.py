# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='db_status',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('status', models.DateTimeField(max_length=50)),
            ],
            options={
                'db_table': 'status',
            },
        ),
    ]
