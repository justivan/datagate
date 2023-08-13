from django.contrib import admin
from .models import HotelMapping, HotelRoomMapping, OperatorMapping


@admin.register(HotelMapping)
class HotelMappingAdmin(admin.ModelAdmin):
    list_display = ("get_hotel_id", "id", "hotel_name", "is_active", "is_charter")
    list_filter = ("hotel__area__region__country__name",)
    list_per_page = 20
    search_fields = ("id", "hotel_name")

    def get_hotel_id(self, obj):
        return obj.hotel.id if obj.hotel else None

    get_hotel_id.short_description = "Master Hotel ID"


@admin.register(HotelRoomMapping)
class HotelRoomMappingAdmin(admin.ModelAdmin):
    list_display = ("room_type", "room_code", "get_hotel_name", "hotel_room")
    search_fields = ("hotel_room__hotel__id",)

    def get_hotel_name(self, obj):
        return obj.hotel_room.hotel.name if obj.hotel_room else None

    get_hotel_name.short_description = "Hotel Name"


@admin.register(OperatorMapping)
class OperatorMappingAdmin(admin.ModelAdmin):
    list_display = ("operator", "external_id", "external_name")
