from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from .models import RentRequest
from .serializers import RentRequestSerializer
from rest_framework.decorators import action
from django.http import Http404
from rest_framework.response import Response
from api.user.models import User
from api.room.models import Room
from api.notification.models import Notification
from datetime import datetime
from django.http import JsonResponse

# Create your views here.


class TenantProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.tenant == request.user


class LandlordProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.landlord == request.user


class RentRequestViewSet(viewsets.ModelViewSet):
    queryset = RentRequest.objects.all()
    serializer_class = RentRequestSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated(), ]

        if self.action == 'get_all_request_from_tenant' or self.action == 'get_confirm_request_from_tenant' or self.action == 'cancel_rent_request':
            return [permissions.IsAuthenticated(), TenantProfilePermission()]

        if self.action == 'get_all_request_from_landlord' or self.action == 'confirm_rent_request' or self.action == 'reject_rent_request':
            return [permissions.IsAuthenticated(), LandlordProfilePermission()]

        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        rent_request_data = request.data

        try:
            room = Room.objects.get(id=rent_request_data["room"])
            tenant = request.auth.user
            landlord = room.house.landlord
        except Room.DoesNotExist:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Cant find room with this id!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Cant find room with this id!")

        if tenant == landlord:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Cant create request with this room!")

        if tenant.balance >= room.totalPrice:
            new_rent_request = RentRequest.objects.create(
                room=room,
                landlord=landlord,
                message=rent_request_data["message"],
                price=room.totalPrice,
                isConfirm=False,
                tenant=tenant,
            )

            new_rent_request.save()

            tenant.balance = tenant.balance - room.totalPrice

            tenant.save()

            tenant_notification = Notification.objects.create(
                user=tenant,
                message="Your rental request has been sent, your account is deducted " +
                str(room.totalPrice)
            )

            tenant_notification.save()

            landlord_notification = Notification.objects.create(
                user=landlord,
                message="You have 1 room rental request from " + tenant.username
            )

            landlord_notification.save()

            serializer = RentRequestSerializer(new_rent_request)

            # return JsonResponse(
            #     {'status': "Ok", 'data': serializer.data})

            return Response(status=status.HTTP_200_OK, data=serializer.data)

        else:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Your balance is not enough to take this action!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Your balance is not enough to take this action!")

    @action(methods=['get'], detail=True, url_path="confirm_rent_request")
    def confirm_rent_request(self, request, pk, *args, **kwargs):
        try:
            rent_request = RentRequest.objects.get(
                id=pk, isConfirm=False, expires_at__gt=datetime.now())
        except RentRequest.DoesNotExist:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Something went wrong!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Something went wrong!")

        landlord = request.auth.user
        room = rent_request.room

        request_list = RentRequest.objects.all().filter(
            room=rent_request.room).exclude(id=pk)

        if rent_request.landlord == landlord:
            rent_request.isConfirm = True
            rent_request.save()

            landlord.balance = landlord.balance + rent_request.price
            landlord.save()

            room.status = "unavailable"
            room.save()

            for request in list(request_list):
                tenant = User.objects.get(username=request.tenant)
                tenant.balance = tenant.balance + rent_request.price
                tenant.save()
                request.delete()

                new_notification = Notification.objects.create(
                    user=tenant,
                    message="Your rental request has been denied"
                )

                new_notification.save()

            new_notification = Notification.objects.create(
                user=rent_request.tenant,
                message="Your tenancy request has been accepted by the landlord"
            )

            new_notification.save()

            # return JsonResponse(
            #     {'status': "Ok", 'data': "Confirm rent request succesfull!"})
            return Response(status=status.HTTP_200_OK, data="Confirm rent request succesfull!")

        else:
            # return JsonResponse(
            #     {'status': "Ok", 'data': "Cant confirm rent request with this id!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Cant confirm rent request with this id!")

        # return Response(status=status.HTTP_200_OK, data="Confirm rent request succesfull!")

    @action(methods=['get'], detail=True, url_path="reject_rent_request")
    def reject_rent_request(self, request, pk, *args, **kwargs):
        try:
            rent_request = RentRequest.objects.get(
                id=pk, isConfirm=False, expires_at__gt=datetime.now())
        except RentRequest.DoesNotExist:
            # return JsonResponse(
            #     {'status': "fail", 'data': "Something went wrong!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Cant find rent request with this id!")

        landlord = request.auth.user
        tenant = User.objects.get(username=rent_request.tenant)

        if rent_request.landlord == landlord:
            tenant.balance = tenant.balance + rent_request.price
            tenant.save()
            rent_request.delete()

            new_notification = Notification.objects.create(
                user=rent_request.tenant,
                message="Your rental request has been denied"
            )

            new_notification.save()

            # return JsonResponse(
            #     {'status': "Ok", 'data': "Reject rent request succesfull!"})
            return Response(status=status.HTTP_200_OK, data="Reject rent request succesfull!")
        else:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Cant reject rent request with this id!"})
            return Response(status=status.HTTP_200_OK, data="Cant reject rent request with this id!")

        return Response(status=status.HTTP_200_OK, data="Reject rent request succesfull!")

    @action(methods=['get'], detail=True, url_path="cancel_rent_request")
    def cancel_rent_request(self, request, pk, *args, **kwargs):
        try:
            rent_request = RentRequest.objects.get(
                id=pk, isConfirm=False, expires_at__gt=datetime.now())
        except RentRequest.DoesNotExist:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Cant find rent request with this id!"})
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Cant find rent request with this id!")

        tenant = request.auth.user

        if rent_request.tenant == tenant:
            tenant.balance = tenant.balance + rent_request.price
            tenant.save()
            rent_request.delete()
            # return JsonResponse(
            #     {'status': "Ok", 'data': "Cancel rent request succesfull!"})
            return Response(status=status.HTTP_200_OK, data="Cancel rent request succesfull!")
        else:
            # return JsonResponse(
            #     {'status': "Fail", 'data': "Cant cancel rent request with this id!"})
            return Response(status=status.HTTP_200_OK, data="Cant cancel rent request with this id!")

    @action(methods=['get'], detail=False, url_path="get_all_request_from_tenant")
    def get_all_request_from_tenant(self, request, *args, **kwargs):
        tenant = request.auth.user
        request_list = RentRequest.objects.all().filter(
            tenant=tenant, isConfirm=False, expires_at__gt=datetime.now())

        try:
            page = self.paginate_queryset(request_list)
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

        serializer = RentRequestSerializer(request_list)

        return Response(self.serializer_class(request_list, many=True, context={"request": request}).data)

    @action(methods=['get'], detail=False, url_path="get_confirm_request_from_tenant")
    def get_confirm_request_from_tenant(self, request, *args, **kwargs):
        tenant = request.auth.user
        request_list = RentRequest.objects.all().filter(
            tenant=tenant, isConfirm=True, expires_at__gt=datetime.now())

        try:
            page = self.paginate_queryset(request_list)
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

        serializer = RentRequestSerializer(request_list)

        return Response(self.serializer_class(request_list, many=True, context={"request": request}).data)

    @action(methods=['get'], detail=False, url_path="get_all_request_from_landlord")
    def get_all_request_from_landlord(self, request, *args, **kwargs):
        landlord = request.auth.user
        request_list = RentRequest.objects.all().filter(
            landlord=landlord, isConfirm=False,  expires_at__gt=datetime.now())

        try:
            page = self.paginate_queryset(request_list)
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

        return Response(self.serializer_class(request_list, many=True, context={"request": request}).data)
