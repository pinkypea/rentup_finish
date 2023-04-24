from rest_framework import viewsets, permissions
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.response import Response

# Create your views here.


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def list(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(
            user=request.auth.user).order_by('-updated_at')
        serializer = NotificationSerializer(queryset, many=True)
        return Response(serializer.data)
