from django.db import models

from accommodation.models import HotelRoom
from clients.models import AllocationGroup
from accounts.models import UserTrackingMixin

from django.db.models.signals import pre_save
from django.dispatch import receiver


class RoomInventory(models.Model):
    BASIS_CHOICES = (
        ("freesale", "Freesale"),
        ("allocation", "Allocation"),
        ("on_request", "On Request"),
    )

    room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    quantity = models.PositiveIntegerField(null=True, blank=True)
    basis = models.CharField(max_length=20, choices=BASIS_CHOICES)
    charter = models.BooleanField(default=False, db_index=True)
    allocation_group = models.ForeignKey(
        AllocationGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    class Meta:
        db_table = "reports_room_inventory"
        ordering = ("room__hotel__name", "room__name", "start_date", "end_date")
        verbose_name_plural = "room inventory"

    def __str__(self):
        return f"{self.room.hotel.name} - {self.room.name}"


class RoomInventoryTopUp(UserTrackingMixin, models.Model):
    room_inventory = models.ForeignKey(RoomInventory, on_delete=models.CASCADE)
    additional_rooms = models.PositiveIntegerField()

    class Meta:
        db_table = "reports_room_inventory_topup"
        ordering = ("room_inventory", "created_at")
        verbose_name_plural = "room inventory topup"

    def __str__(self):
        return f"{self.room_inventory.room}"


@receiver(pre_save, sender=RoomInventory)
def update_quantity(sender, instance, **kwargs):
    if instance.basis == "freesale":
        instance.quantity = 0
    elif instance.basis == "on_request":
        instance.quantity = 0
