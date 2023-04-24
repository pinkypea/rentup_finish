from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "city", "district", "ward",
                    "phone", "linkfb", "linkin", "linktw", "linkli", "balance", "forgetPasswordToken", "image"]
    search_fields = ["id", "username", "city", "district", "ward",
                     "phone", "linkfb", "linkin", "linktw", "linkli", "balance", "forgetPasswordToken", "image"]
    list_filter = ["id", "username", "city", "district", "ward",
                   "phone", "linkfb", "linkin", "linktw", "linkli", "balance", "forgetPasswordToken", "image"]


# Register your models here.
admin.site.register(User, UserAdmin)
