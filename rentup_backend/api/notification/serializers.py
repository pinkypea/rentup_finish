from rest_framework.serializers import ModelSerializer
from .models import Notification
from api.user.serializers import UserSerializer
from api.user.models import User
from api.rent_request.serializers import RentRequestSerializer
from api.rent_request.models import RentRequest
from api.serializers import RelatedFieldAlternative


class NotificationSerializer(ModelSerializer):
    user = RelatedFieldAlternative(
        queryset=User.objects.all(), serializer=UserSerializer)

    rentRequest = RelatedFieldAlternative(
        queryset=RentRequest.objects.all(), serializer=RentRequestSerializer)

    class Meta:
        model = Notification
        fields = '__all__'
