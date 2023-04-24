from django.db import models
from api.category.models import Category
from api.user.models import User

# Create your models here.


class House(models.Model):
    city = models.CharField(max_length=250)
    district = models.CharField(max_length=250)
    ward = models.CharField(max_length=250)
    address = models.CharField(max_length=750)
    detail = models.CharField(max_length=250)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='house/%Y/%m')

    landlord = models.ForeignKey(
        User, related_name='landlord', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.address = self.city + ' ' + self.district + ' ' + self.ward
        super(House, self).save(*args, **kwargs)

    def __str__(self):
        return self.address
