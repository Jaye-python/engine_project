from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "total", "items_count")
    list_filter = ("items_count",)
    search_fields = ("id",)
    list_editable = ("total", "items_count")
    actions = ["delete_selected"]
