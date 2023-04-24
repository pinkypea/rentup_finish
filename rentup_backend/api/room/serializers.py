from rest_framework.serializers import ModelSerializer
from .models import Room
from api.house.serializers import HouseSerializer
from api.category.serializers import CategorySerializer
from api.house.models import House
from api.category.models import Category
from api.serializers import RelatedFieldAlternative


class RoomSerializer(ModelSerializer):
    house = RelatedFieldAlternative(
        queryset=House.objects.all(), serializer=HouseSerializer)
    category = RelatedFieldAlternative(
        queryset=Category.objects.all(), serializer=CategorySerializer)

    class Meta:
        model = Room
        fields = "__all__"
