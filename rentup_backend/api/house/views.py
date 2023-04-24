from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import House
from .serializers import HouseSerializer
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.response import Response
from api.user.models import User
from api.category.models import Category
from django.http import JsonResponse

# Create your views here.


class OwnProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.landlord == request.user


class HouseViewSet(viewsets.ModelViewSet):
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [permissions.IsAuthenticated, OwnProfilePermission]

    def create(self, request, *args, **kwargs):
        house_data = request.data

        try:
            category = Category.objects.get(name=house_data["category"])
        except Category.DoesNotExist:
            # response = JsonResponse(
            #     {'status': "Fail", 'data': "Cant create house with this category!"})

            # return response
            return Response(status=status.HTTP_404_NOT_FOUND, data="Cant find create house with this category!")

        new_house = House.objects.create(
            category=category,
            city=house_data["city"],
            district=house_data["district"],
            ward=house_data["ward"],
            detail=house_data["detail"],
            description=house_data["description"],
            image=house_data["image"],
            landlord=request.auth.user,
        )

        new_house.save()

        serializer = HouseSerializer(new_house)

        # return JsonResponse({'status': "Ok", 'data': serializer.data})

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=['get'], detail=False, url_path="get_owned_house")
    def get_owned_house(self, request):
        try:
            user = request.auth.user
            house = House.objects.filter(landlord=user.id)

            try:
                page = self.paginate_queryset(house)
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
            return Response("user id is invalid", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(self.serializer_class(house, many=True, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)
