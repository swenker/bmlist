# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-22 06:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('subtitle', models.CharField(blank=True, max_length=60, null=True)),
                ('isbn10', models.CharField(blank=True, max_length=10, null=True)),
                ('isbn13', models.CharField(blank=True, max_length=13, null=True)),
                ('author', models.CharField(max_length=80)),
                ('transtr', models.CharField(blank=True, max_length=100, null=True)),
                ('publisher', models.CharField(max_length=60)),
                ('pubdate', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pages', models.IntegerField(default=0)),
                ('update_time', models.DateTimeField(auto_now_add=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.SmallIntegerField(default=1)),
                ('binding', models.CharField(blank=True, max_length=10, null=True)),
                ('series', models.CharField(blank=True, max_length=40, null=True)),
                ('keywords', models.CharField(blank=True, max_length=40, null=True)),
                ('summary', models.CharField(blank=True, max_length=500, null=True)),
                ('authorintro', models.CharField(blank=True, max_length=500, null=True)),
                ('status', models.SmallIntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=60)),
                ('passwd', models.CharField(max_length=20)),
                ('nickname', models.CharField(blank=True, max_length=20, null=True)),
                ('cellphone', models.CharField(max_length=20)),
                ('status', models.SmallIntegerField(default=1)),
            ],
        ),
    ]
