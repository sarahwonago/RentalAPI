from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsLandLord

from .models import Building
from .serializers import BuildingSerializer


class BuildingViewSet(ModelViewSet):
    """
    Viewset for managing buildings.

    Only authenticated landlord can access this endpoints.
    """
    permission_classes = [IsAuthenticated, IsLandLord]
    serializer_class = BuildingSerializer

    def get_queryset(self):
        # fetch buildings for the current logged in landlord
        buildings = Building.objects.filter(
            landlord=self.request.user
        )
        return buildings
    
    def perform_create(self, serializer):
        # creates a building and links it to the logged in landlord
        serializer.save(landlord=self.request.user)