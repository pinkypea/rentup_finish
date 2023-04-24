from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from .models import Category
from .serializers import CategorySerializer

# Create your views here.


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]

        return [permissions.IsAdminUser()]
