from rest_framework.routers import DefaultRouter

from .views import BuildingViewSet

router = DefaultRouter()
router.register(r"building", BuildingViewSet, basename="buildings")

urlpatterns = router.urls
