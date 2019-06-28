# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-07-02 06:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("variants", "0047_auto_20190701_1625"), ("svs", "0003_auto_20190619_1529")]

    operations = [
        migrations.CreateModel(
            name="StructuralVariantSet",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                (
                    "date_created",
                    models.DateTimeField(auto_now_add=True, help_text="DateTime of creation"),
                ),
                (
                    "date_modified",
                    models.DateTimeField(auto_now=True, help_text="DateTime of last modification"),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("importing", "importing"),
                            ("active", "active"),
                            ("deleting", "deleting"),
                        ],
                        max_length=16,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="structuralvariant",
            name="chromosome_no",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="structuralvariant",
            name="set_id",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="structuralvariantgeneannotation",
            name="case_id",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="structuralvariantgeneannotation",
            name="set_id",
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="structuralvariant",
            index=models.Index(fields=["set_id"], name="svs_structu_set_id_951ec1_idx"),
        ),
        migrations.AddIndex(
            model_name="structuralvariantgeneannotation",
            index=models.Index(fields=["set_id"], name="svs_structu_set_id_42f2ba_idx"),
        ),
        migrations.AddField(
            model_name="structuralvariantset",
            name="case",
            field=models.ForeignKey(
                help_text="The case that this set is for",
                on_delete=django.db.models.deletion.CASCADE,
                to="variants.Case",
            ),
        ),
    ]