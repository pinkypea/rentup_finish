from django.db import models
from api.room.models import Room
from api.user.models import User
from datetime import datetime, timedelta

# Create your models here.


def get_expried():
    return datetime.now()+timedelta(days=30)


class RentRequest(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.PROTECT, related_name='rent_request')
    tenant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rent_request_tenant')
    landlord = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rent_request_landlord')
    message = models.CharField(max_length=250)
    isConfirm = models.BooleanField(default=False)
    price = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(
        null=True, blank=True, default=get_expried)

    def save(self, *args, **kwargs):
        self.expires_at = datetime.now()+timedelta(days=30)
        super(RentRequest, self).save(*args, **kwargs)
