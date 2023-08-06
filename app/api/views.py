from rest_framework.generics import ListAPIView
from django.contrib.gis.geos import Point

from definitions.models import Country, Region, Area
from definitions.serializers import CountrySerializer, RegionSerializer, AreaSerializer


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class RegionListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class AreaListAPIView(ListAPIView):
    serializer_class = AreaSerializer

    def get_queryset(self):
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")

        if lat is not None and lng is not None:
            point = Point(float(lng), float(lat), srid=4326)
            queryset = Area.objects.filter(geom__contains=point)
        else:
            queryset = Area.objects.all()

        return queryset
