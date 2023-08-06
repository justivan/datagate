from django.urls import path
from .views import CountryListAPIView, RegionListAPIView, AreaListAPIView

app_name = "api"
urlpatterns = [
    path("country/", CountryListAPIView.as_view(), name="country-list"),
    path("region/", RegionListAPIView.as_view(), name="country-list"),
    path("area/", AreaListAPIView.as_view(), name="country-list"),
]
