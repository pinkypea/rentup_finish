from django.db import models
from api.user.models import User
from api.rent_request.models import RentRequest

# Create your models here.


class Notification(models.Model):
    message = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rentRequest = models.ForeignKey(
        RentRequest, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
