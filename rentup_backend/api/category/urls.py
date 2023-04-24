from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.CategoryViewSet)


# /category/ - GET
# /category/ - POST
# /category/{category_id} - GET
# /category/{category_id} - PUT
# /category/{category_id} - DELETE
urlpatterns = [
    path('', include(router.urls))
]
