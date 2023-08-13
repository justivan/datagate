from django.db import models
from django.utils.translation import gettext_lazy as _
from accommodation.models import Hotel, HotelRoom
from clients.models import Operator


class HotelMapping(models.Model):
    id = models.IntegerField(_("GWG Hotel ID"), primary_key=True)
    hotel = models.ForeignKey(
        Hotel,
        verbose_name=_("Master Hotel Name"),
        on_delete=models.PROTECT,
    )
    hotel_name = models.CharField(_("GWG Hotel Name"), max_length=120)
    is_charter = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("hotel__name", "hotel_name")
        db_table = "mapping_hotel"
        verbose_name_plural = "hotel mapping"

    def __str__(self):
        return f"{self.hotel_name}"


class HotelRoomMapping(models.Model):
    hotel_room = models.ForeignKey(HotelRoom, on_delete=models.PROTECT)
    room_type = models.CharField(_("GWG Room Type"), max_length=50)
    room_code = models.CharField(_("GWG Room Code"), max_length=50)

    class Meta:
        ordering = ("hotel_room__hotel__name", "hotel_room")
        db_table = "mapping_hotel_room"
        verbose_name_plural = "room mapping"
        unique_together = (("hotel_room", "room_type"),)

    def __str__(self):
        return f"{self.room_type}"


class OperatorMapping(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.PROTECT)
    external_id = models.IntegerField(_("GWG Operator ID"), unique=True)
    external_name = models.CharField(_("GWG Operator Name"), unique=True, max_length=120)

    class Meta:
        ordering = ("external_name",)
        db_table = "mapping_operator"
        verbose_name_plural = "operator mapping"

    def __str__(self):
        return f"{self.external_id} - {self.external_name}"
