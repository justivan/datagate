from django.db import models
from django.contrib.gis.db.models import MultiPolygonField
from django.utils.translation import gettext_lazy as _


class Country(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=120, unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        to_field="code",
        db_column="country_code",
    )

    class Meta:
        ordering = ("country", "name")

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=120)
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    geom = MultiPolygonField(srid=4326)

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "name__icontains")

    class Meta:
        ordering = ("name",)
        unique_together = (("name", "region"),)

    def __str__(self):
        return self.name


class MealPlan(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = "definitions_meal_plan"
        ordering = ("name",)

    def __str__(self):
        return self.name
