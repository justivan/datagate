from django.contrib import admin
from .models import Operator, OperatorGroup
from mapping.models import OperatorMapping


class OperatorInline(admin.TabularInline):
    model = Operator
    extra = 0


class OperatorMappingInline(admin.TabularInline):
    model = OperatorMapping
    extra = 0


@admin.register(Operator)
class OperatorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "short_name",
        "category",
        "operator_group",
    )
    list_filter = ("name", "category")
    search_fields = ("name",)
    inlines = (OperatorMappingInline,)

    def operator_group(self, obj):
        return obj.operator_group


@admin.register(OperatorGroup)
class OperatorAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "operators",
    )
    inlines = (OperatorInline,)

    def operators(self, obj):
        operators = Operator.objects.filter(operator_group=obj)
        operator_names = ", ".join(operator.name for operator in operators)
        return operator_names if operator_names else "-"
