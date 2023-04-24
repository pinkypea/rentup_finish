from rest_framework.serializers import ModelSerializer
from .models import User


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(user.password)
        user.address = user.city + ' ' + user.district + ' ' + user.ward
        user.save()

        return user

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "image",
                  "username", "password", "email", "phone", "city", "district", "ward", "linkfb", "linkin", "linktw", "linkli", "balance"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }
