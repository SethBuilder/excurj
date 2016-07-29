# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', unique=True, max_length=128)),
                ('country', models.CharField(default=b'Scotland', max_length=128)),
                ('information', models.CharField(default=b'', max_length=3000)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hobby', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(max_length=128)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profilepic', models.ImageField(upload_to=b'static/images/Profile Pictures', blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('average_rating', models.IntegerField(default=0)),
                ('ratings_count', models.IntegerField(default=0)),
                ('city', models.ForeignKey(to='mainapp.City')),
                ('hobbies', models.ManyToManyField(to='mainapp.Hobby')),
                ('languages', models.ManyToManyField(to='mainapp.Language')),
                ('user', models.OneToOneField(related_name=b'profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=500, blank=True)),
                ('rating', models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)])),
                ('rating_user', models.ForeignKey(related_name=b'rating_user', to='mainapp.UserProfile')),
                ('user', models.ForeignKey(related_name=b'rated_user', to='mainapp.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
