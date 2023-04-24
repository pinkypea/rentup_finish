from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "image", "created_at", "updated_at"]
    search_fields = ["id", "name"]
    list_filter = ["id", "name"]


# Register your models here.
admin.site.register(Category, CategoryAdmin)
