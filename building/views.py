from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter

from account.permissions import IsLandLord

from .models import Building, House
from .serializers import BuildingSerializer, HouseSerializer


@extend_schema_view(
    create=extend_schema(
        summary="Creates a new building",
        description="Create a new building.",
        responses={201: BuildingSerializer},
        request=BuildingSerializer,
        tags=['building management']
    ),
    list=extend_schema(
        summary="List all buildings",
        description="Retrieve a list of all buildings linked to the authenticated landlord.",
        responses={200: BuildingSerializer(many=True)},
        tags=['building management']
    ),
    retrieve=extend_schema(
        summary="Retrieve a building",
        description="Retrieve details of a specific building by UUID.",
        responses={200: BuildingSerializer},
        tags=['building management']
    ),
    update=extend_schema(
        summary="Update a building",
        description="Update details of a specific building.",
        responses={200: BuildingSerializer},
        tags=['building management']
    ),
    partial_update=extend_schema(
        summary="Update a building partially",
        description="Update details of a specific building partially.",
        responses={200: BuildingSerializer},
        tags=['building management']
    ),
    destroy=extend_schema(
        summary="Delete a building",
        description="Delete a specific building.",
        responses={204: None},
        tags=['building management']
    ),
)
class BuildingViewSet(ModelViewSet):
    """
    Viewset for managing buildings.

    Only authenticated landlord can access this endpoints.
    """
    permission_classes = [IsAuthenticated, IsLandLord]
    serializer_class = BuildingSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]

    
    filterset_fields = ["name", "address"]
    search_fields = ["name"]
    ordering_fields = ['name']
    ordering = ['name']

    def get_queryset(self):
        # fetch buildings for the current logged in landlord
        buildings = Building.objects.filter(
            landlord=self.request.user
        )
        return buildings
    
    def perform_create(self, serializer):
        # creates a building and links it to the logged in landlord
        serializer.save(landlord=self.request.user)



@extend_schema_view(
    create=extend_schema(
        summary="Creates a new house",
        description="Create a new house in a building.",
        responses={201: HouseSerializer},
        request=HouseSerializer,
        tags=['house management']
    ),
    list=extend_schema(
        summary="List all houses in a building",
        description="Retrieve a list of all houses in a building.",
        responses={200: HouseSerializer(many=True)},
        tags=['house management']
    ),
    retrieve=extend_schema(
        summary="Retrieve a house",
        description="Retrieve details of a specific house by UUID.",
        responses={200: HouseSerializer},
        tags=['house management']
    ),
    update=extend_schema(
        summary="Update a house",
        description="Update details of a specific house.",
        responses={200: HouseSerializer},
        tags=['house management']
    ),
    partial_update=extend_schema(
        summary="Update a house partially",
        description="Update details of a specific house partially.",
        responses={200: HouseSerializer},
        tags=['house management']
    ),
    destroy=extend_schema(
        summary="Delete a house",
        description="Delete a specific house.",
        responses={204: None},
        tags=['house management']
    ),
)
class HouseViewSet(ModelViewSet):
    """
    Viewset for managing houses within a specific building.

    Only authenticated landlord can access this endpoints.
    """
    permission_classes = [IsAuthenticated, IsLandLord]
    serializer_class = HouseSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    
    filterset_fields = ["name", "is_occupied"]
    search_fields = ["name"]
    ordering_fields = ['name']
    ordering = ['is_occupied']

    def get_queryset(self):
        """
        Filter the queryset to only include houses belonging to a specific building.
        """
        building_id = self.kwargs.get('building_id')

        # Verify the building exists and belongs to the current landlord
        try:
            building = Building.objects.get(id=building_id, landlord=self.request.user)
        except Building.DoesNotExist:
            raise PermissionDenied("You do not have permission to access this building.")

        # Filter houses to only include those under the specified building
        return House.objects.filter(building=building)
        
    def perform_create(self, serializer):
        """
        Create a house and link it to a building.
        """
        building_id = self.kwargs.get('building_id')
        building = Building.objects.get(
            id=building_id,
            landlord=self.request.user)
        serializer.save(building=building)

    @extend_schema(
    summary="Mark a house as vacant",
    description="Mark a house as vacant.",
    responses={200: "House marked vacant"},
    tags=['house management']
    )
    @action(detail=True, methods=['post'])
    def mark_vacant(self, request, pk=None, building_id=None):
        """
        Mark a house as vacant.
        """
        house = self.get_object()
        house.is_occupied = False
        house.save()
        return Response({"message":"House marked vacant"},status=status.HTTP_200_OK)