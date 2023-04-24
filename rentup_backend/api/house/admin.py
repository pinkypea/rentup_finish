from django.contrib import admin
from .models import House


class HouseAdmin(admin.ModelAdmin):
    list_display = ["id", "landlord", "city", "district", "ward",
                    "address", "detail", "description", "category", "image", "created_at", "updated_at"]
    search_fields = ["id", "landlord", "city", "district", "ward",
                     "address", "detail", "description", "category", "image", "created_at", "updated_at"]
    list_filter = ["id", "landlord", "city", "district", "ward",
                   "address", "detail", "description", "category", "image", "created_at", "updated_at"]


# Register your models here.
admin.site.register(House, HouseAdmin)
