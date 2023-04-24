from rest_framework import viewsets, permissions, status
from .models import Room
from .serializers import RoomSerializer
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.response import Response
from datetime import datetime

# Create your views here.


class OwnProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.house.landlord == request.user


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all().filter()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'get_room_available':
            return [permissions.AllowAny()]

        return [permissions.IsAuthenticated(), OwnProfilePermission()]

    def list(self, request, *args, **kwargs):
        queryset = Room.objects.filter(active=True).exclude(
            rent_request__isConfirm=True, rent_request__expires_at__gt=datetime.now())

        city = self.request.query_params.get('city', None)
        district = self.request.query_params.get('district', None)
        ward = self.request.query_params.get('ward', None)
        category = self.request.query_params.get('category', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)

        if city:  # check if key is not None
            queryset = queryset.filter(house__city=city)

        if district:  # check if key is not None
            queryset = queryset.filter(house__district=district)

        if ward:  # check if key is not None
            queryset = queryset.filter(house__ward=ward)

        if category:  # check if key is not None
            queryset = queryset.filter(category__name=category)

        if min_price:  # check if key is not None
            queryset = queryset.filter(totalPrice__gte=min_price)

        if max_price:  # check if key is not None
            queryset = queryset.filter(totalPrice__lte=max_price)

        try:
            page = self.paginate_queryset(queryset)
        except Exception as e:
            page = []
            data = page
            return Response({
                "status": status.HTTP_200_OK,
                "message": 'No more record.',
                "data": data
            })

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            return self.get_paginated_response(data)

        # # serializer = self.get_serializer(queryset, many=True)
        # return Response({
        #     "status": status.HTTP_200_OK,
        #     "message": 'Sitting records.',
        #     "data": data
        # })

        serializer = RoomSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['get'], detail=True, url_path="get_room_list_of_house")
    def get_room_list_of_house(self, request, pk):
        try:
            rooms = Room.objects.all().filter(house=pk)
            try:
                page = self.paginate_queryset(rooms)
            except Exception as e:
                page = []
                data = page
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": 'No more record.',
                    "data": data
                })

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                return self.get_paginated_response(data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(self.serializer_class(rooms, many=True, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

    @action(methods=['get'], detail=False, url_path="get_room_available")
    def get_room_available(self, request):
        try:
            rooms = Room.objects.all().exclude(rentrequest__isConfirm=True)
            try:
                page = self.paginate_queryset(rooms)
            except Exception as e:
                page = []
                data = page
                return Response({
                    "status": status.HTTP_200_OK,
                    "message": 'No more record.',
                    "data": data
                })

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                return self.get_paginated_response(data)
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(self.serializer_class(rooms, many=True, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)
