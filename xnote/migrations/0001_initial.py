# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-07 03:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='XNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=60, null=True)),
                ('content', models.TextField(blank=True, max_length=2000, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('uid', models.IntegerField(default=0)),
                ('status', models.SmallIntegerField(default=1)),
            ],
        ),
    ]