# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-07 13:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("variants", "0050_auto_20190731_1109")]

    operations = [
        migrations.AddField(
            model_name="case",
            name="notes",
            field=models.CharField(blank=True, default="", max_length=2048, null=True),
        )
    ]