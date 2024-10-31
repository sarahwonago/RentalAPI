from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet, HouseViewSet

router = DefaultRouter()
router.register(r"buildings", BuildingViewSet, basename="buildings")


urlpatterns = [
    path('buildings/<uuid:building_id>/houses/', HouseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='house-list'),
    path('buildings/<uuid:building_id>/houses/<uuid:pk>/', HouseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='house-detail'),
]

urlpatterns += router.urls
