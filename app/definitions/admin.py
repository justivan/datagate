from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin
from .models import Country, Region, Area, MealPlan


@admin.register(Country)
class CountryModelAdmin(admin.ModelAdmin):
    list_display = ("code", "name")


@admin.register(Region)
class RegionModelAdmin(admin.ModelAdmin):
    list_display = ("name", "country")


@admin.register(Area)
class AreaModelAdmin(LeafletGeoAdmin):
    list_display = ("name", "country", "region")
    list_filter = (
        "region__country",
        "region",
    )
    list_per_page = 20
    search_fields = ("name",)

    def country(self, obj):
        return obj.region.country


@admin.register(MealPlan)
class MealPlanModelAdmin(admin.ModelAdmin):
    list_display = ("code", "name")
