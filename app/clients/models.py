from django.db import models
from django.utils.translation import gettext_lazy as _


class OperatorGroup(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        db_table = "clients_operator_group"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Operator(models.Model):
    CATEGORY_CHOICES = (
        ("IC", "IC"),
        ("PP", "PP"),
    )
    name = models.CharField(max_length=120, unique=True)
    short_name = models.CharField(max_length=12)
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    operator_group = models.ForeignKey(
        OperatorGroup,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    @staticmethod
    def autocomplete_search_fields():
        return (
            "id__iexact",
            "name__icontains",
        )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
