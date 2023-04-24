from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.RoomViewSet)


# /room/ - GET
# /room/ - POST
# /room/{room_id} - GET
# /room/{room_id} - PUT
# /room/{room_id} - DELETE
urlpatterns = [
    path('', include(router.urls))
]
