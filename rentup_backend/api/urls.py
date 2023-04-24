from django.urls import path, include
from . import views

urlpatterns = [
    path('oauth2-info/', views.AuthInfo.as_view()),
    path('category/', include('api.category.urls')),
    path('house/', include('api.house.urls')),
    path('room/', include('api.room.urls')),
    path('user/', include('api.user.urls')),
    path('rent_request/', include('api.rent_request.urls')),
    path('notification/', include('api.notification.urls')),
]
