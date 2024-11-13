from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


from drf_spectacular.utils import extend_schema, extend_schema_view

from account.permissions import IsLandLord

from building.models import House

from .models import Lease
from .serializers import LeaseSerializer

User = get_user_model()


@extend_schema_view(
    create=extend_schema(
        summary="Creates a new lease",
        description="Create a new lease.",
        responses={201: LeaseSerializer},
        request=LeaseSerializer,
        tags=['lease management']
    ),
    list=extend_schema(
        summary="List all leases",
        description="Retrieve a list of all leases.",
        responses={200: LeaseSerializer(many=True)},
        tags=['lease management']
    ),
    retrieve=extend_schema(
        summary="Retrieve a lease",
        description="Retrieve details of a specific lease by UUID.",
        responses={200: LeaseSerializer},
        tags=['lease management']
    ),
    update=extend_schema(
        summary="Update a lease",
        description="Update details of a specific lease.",
        responses={200: LeaseSerializer},
        tags=['lease management']
    ),
    partial_update=extend_schema(
        summary="Update a lease partially",
        description="Update details of a specific lease partially.",
        responses={200: LeaseSerializer},
        tags=['lease management']
    ),
    destroy=extend_schema(
        summary="Delete a lease",
        description="Delete a specific lease.",
        responses={204: None},
        tags=['lease management']
    ),
)
class LeaseViewSet(viewsets.ModelViewSet):
    """
    Viwset for the Lease model.
    """

    permission_classes = [IsAuthenticated, IsLandLord]
    serializer_class = LeaseSerializer

    def get_queryset(self):
        # Allow landlords to view leases that belong to their tenants only.
        return Lease.objects.filter(house__building__landlord=self.request.user)
    
    def create(self, request, *args, **kwargs):

        tenant_id = request.data.get("tenant")
        house_id = request.data.get("house")

        # validate the tenant is linked to landlord
        tenant = get_object_or_404(User, id=tenant_id, tenant__landlord=request.user)

        # ensure the tenant does not have an active lease
        if Lease.objects.filter(tenant=tenant, is_active=True).exists():
            raise ValidationError("Tenant already has an active lease.")
        
        # validate the house is linked to landlord
        house = get_object_or_404(House, id=house_id, building__landlord=request.user)

        # ensure the house is vacant
        if house.is_occupied:
            raise ValidationError("House is already occupied.")
        
        # create the lease
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(house=house, tenant=tenant)
        #self.perform_create(serializer)

        # mark the house as occupied
        house.is_occupied = True
        house.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        """
        saves the lease with default values.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Custom delete method to mark the house as vacant when lease is deleted.
        """

        # mark the house as vacant if the lease is active
        if instance.is_active:
            instance.house.is_occupied = False
            instance.house.save()
        instance.delete()
