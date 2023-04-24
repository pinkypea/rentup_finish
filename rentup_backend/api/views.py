from django.shortcuts import render
from rest_framework.response import Response
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)
