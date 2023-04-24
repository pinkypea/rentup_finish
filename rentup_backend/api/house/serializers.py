from rest_framework.serializers import ModelSerializer
from .models import House
from api.category.serializers import CategorySerializer
from api.user.serializers import UserSerializer
from api.user.models import User
from api.category.models import Category
from api.serializers import RelatedFieldAlternative


class HouseSerializer(ModelSerializer):
    landlord = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)
    category = RelatedFieldAlternative(
        queryset=Category.objects.all(), serializer=CategorySerializer)

    class Meta:
        model = House
        exclude = ('address', )
