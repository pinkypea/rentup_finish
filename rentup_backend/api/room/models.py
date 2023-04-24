from django.db import models
from api.house.models import House
from api.category.models import Category

# Create your models here.


class Room(models.Model):
    class Meta:
        # unique_together -> chi co 1 cap name - house
        unique_together = ('name', 'house')

    name = models.CharField(max_length=250)
    area = models.IntegerField()
    rentPrice = models.IntegerField()
    waterPrice = models.IntegerField()
    electricPrice = models.IntegerField()
    servicePrice = models.IntegerField()
    totalPrice = models.IntegerField(default=0)
    detail = models.TextField(null=True)
    status = models.CharField(max_length=250, default="available")
    active = models.BooleanField(default=False)
    image = models.ImageField(upload_to='room/%Y/%m')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category")
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, related_name="house")

    def save(self, *args, **kwargs):
        self.totalPrice = self.rentPrice + self.waterPrice + \
            self.electricPrice + self.servicePrice
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
