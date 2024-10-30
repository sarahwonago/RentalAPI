from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet, HouseViewSet

router = DefaultRouter()
router.register(r"buildings", BuildingViewSet, basename="buildings")
router.register(r"houses", HouseViewSet, basename="houses")

urlpatterns = router.urls
