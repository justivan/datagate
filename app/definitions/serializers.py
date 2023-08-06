from rest_framework import serializers
from .models import Country, Region, Area


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("code", "name")


class RegionSerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Region
        fields = ("id", "name", "country")


class AreaSerializer(serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Area
        fields = ("id", "name", "region")
