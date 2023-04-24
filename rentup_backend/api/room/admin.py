from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "area", "rentPrice",
                    "waterPrice", "electricPrice", "servicePrice", "detail", "status", "active", "image", "created_at", "updated_at"]
    search_fields = ["id", "name", "area", "rentPrice",
                     "waterPrice", "electricPrice", "servicePrice", "detail", "status", "active", "image", "created_at", "updated_at"]
    list_filter = ["id", "name", "area", "rentPrice",
                   "waterPrice", "electricPrice", "servicePrice", "detail", "status", "active", "image", "created_at", "updated_at"]


# Register your models here.
admin.site.register(Room, RoomAdmin)
