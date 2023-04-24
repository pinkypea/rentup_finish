from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserViewSet)


# /user/ - GET
# /user/ - POST
# /user/{user_id} - GET
# /user/{user_id} - PUT
# /user/{user_id} - DELETE
urlpatterns = [
    path('', include(router.urls))
]
