# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 09:10
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.IntegerField(editable=False, help_text='Wikipedia page id', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=256)),
                ('rvcontinue', models.CharField(blank=True, default='0', max_length=32)),
                ('spam_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.IntegerField(editable=False, help_text='Wikipedia revision id', primary_key=True, serialize=False)),
                ('article_id', models.IntegerField()),
                ('editor', models.CharField(max_length=87)),
                ('timestamp', models.DateTimeField(blank=True, null=True)),
                ('length', models.IntegerField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('position', models.IntegerField()),
                ('original_adds', models.IntegerField()),
                ('token_ids', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RevisionContent',
            fields=[
                ('id', models.IntegerField(editable=False, help_text='Wikipedia revision id', primary_key=True, serialize=False)),
                ('values', models.TextField()),
                ('token_ids', models.TextField()),
                ('rev_ids', models.TextField()),
                ('editors', models.TextField()),
                ('inbound', models.TextField()),
                ('outbound', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('value', models.TextField()),
                ('article_id', models.IntegerField()),
                ('token_id', models.IntegerField()),
                ('origin_rev_id', models.IntegerField()),
                ('editor', models.CharField(default='', help_text='Editor of label revision', max_length=87)),
                ('last_rev_id', models.IntegerField(default=0)),
                ('inbound', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('outbound', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
