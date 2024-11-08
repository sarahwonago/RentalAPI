from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet, HouseViewSet

router = DefaultRouter()
router.register(r"", BuildingViewSet, basename="buildings")


urlpatterns = [
    path('<uuid:building_id>/houses/', HouseViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='house-list'),
    
    path('<uuid:building_id>/houses/<uuid:pk>/', HouseViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='house-detail'),

    # Manually registered route for `mark_vacant` action
    path('<uuid:building_id>/houses/<uuid:pk>/vacant/', HouseViewSet.as_view({
        'post': 'mark_vacant'
    }), name='house-mark-vacant'),
]

urlpatterns += router.urls
