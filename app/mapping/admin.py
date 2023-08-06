from django.contrib import admin
from .models import HotelMapping, HotelRoomMapping


@admin.register(HotelMapping)
class HotelMappingAdmin(admin.ModelAdmin):
    list_display = ("get_hotel_id", "id", "hotel_name", "is_active", "is_charter")
    list_filter = ("hotel__area__region__country__name",)
    list_per_page = 20
    search_fields = ("id", "hotel_name")

    def get_hotel_id(self, obj):
        return obj.hotel.id if obj.hotel else None

    get_hotel_id.short_description = "Master Hotel ID"
