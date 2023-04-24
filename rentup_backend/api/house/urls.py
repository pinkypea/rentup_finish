from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.HouseViewSet)


# /house/ - GET
# /house/ - POST
# /house/{house_id} - GET
# /house/{house_id} - PUT
# /house/{house_id} - DELETE
urlpatterns = [
    path('', include(router.urls))
]
