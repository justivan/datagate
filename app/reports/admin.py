from django.contrib import admin

from clients.models import AllocationGroup
from .models import RoomInventory


@admin.register(RoomInventory)
class RoomInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "room",
        "hotel",
        "start_date",
        "end_date",
        "quantity",
        "basis",
        "charter",
        "allocation_group",
    )

    def hotel(self, obj):
        return obj.room.hotel.name


admin.site.register(AllocationGroup)
