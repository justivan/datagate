# Generated by Django 4.2.2 on 2023-08-05 22:13

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=2, unique=True)),
                ("name", models.CharField(max_length=120, unique=True)),
            ],
            options={
                "verbose_name_plural": "Countries",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="MealPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=3, unique=True)),
                ("name", models.CharField(max_length=60, unique=True)),
            ],
            options={
                "db_table": "definitions_meal_plan",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Region",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120, unique=True)),
                (
                    "country",
                    models.ForeignKey(
                        db_column="country_code",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="definitions.country",
                        to_field="code",
                    ),
                ),
            ],
            options={
                "ordering": ("country", "name"),
            },
        ),
        migrations.CreateModel(
            name="Area",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=120)),
                (
                    "geom",
                    django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326),
                ),
                (
                    "region",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="definitions.region",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "unique_together": {("name", "region")},
            },
        ),
    ]
