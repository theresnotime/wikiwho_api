# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-05 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wikiwho', '0005_auto_20180920_1137'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.DeleteModel(
            name='EditorDataDe',
        ),
        migrations.DeleteModel(
            name='EditorDataDeNotIndexed',
        ),
        migrations.DeleteModel(
            name='EditorDataEn',
        ),
        migrations.DeleteModel(
            name='EditorDataEnNotIndexed',
        ),
        migrations.DeleteModel(
            name='EditorDataEs',
        ),
        migrations.DeleteModel(
            name='EditorDataEsNotIndexed',
        ),
        migrations.DeleteModel(
            name='EditorDataEu',
        ),
        migrations.DeleteModel(
            name='EditorDataEuNotIndexed',
        ),
        migrations.DeleteModel(
            name='EditorDataTr',
        ),
        migrations.DeleteModel(
            name='EditorDataTrNotIndexed',
        ),
    ]
