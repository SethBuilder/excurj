# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='image',
            field=models.ImageField(default=b'', upload_to=b'city_images'),
        ),
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=6),
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.DecimalField(default=0, max_digits=9, decimal_places=6),
        ),
    ]
