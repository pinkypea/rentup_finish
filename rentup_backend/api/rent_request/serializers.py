from rest_framework.serializers import ModelSerializer
from .models import RentRequest
from api.user.serializers import UserSerializer
from api.room.serializers import RoomSerializer
from api.user.models import User
from api.room.models import Room
from api.serializers import RelatedFieldAlternative


class RentRequestSerializer(ModelSerializer):
    landlord = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)
    tenant = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)
    room = RelatedFieldAlternative(
        queryset=Room.objects.all(), serializer=RoomSerializer)

    class Meta:
        model = RentRequest
        fields = '__all__'
