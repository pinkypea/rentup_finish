from attr import s
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='user/%Y/%m', null=True)
    city = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=250, null=True)
    ward = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=750, null=True)
    phone = models.CharField(max_length=10, null=True, unique=True)
    linkfb = models.CharField(max_length=500, null=True, unique=True)
    linkin = models.CharField(max_length=500, null=True, unique=True)
    linktw = models.CharField(max_length=500, null=True, unique=True)
    linkli = models.CharField(max_length=500, null=True, unique=True)
    balance = models.IntegerField(default=0)
    forgetPasswordToken = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if (self.city != None and self.district != None and self.ward != None):
            self.address = self.city + ' ' + self.district + ' ' + self.ward
        super(User, self).save(*args, **kwargs)
