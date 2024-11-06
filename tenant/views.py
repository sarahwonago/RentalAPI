from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated


from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, extend_schema_view

from account.permissions import IsLandLord

from .serializers import TenantRegistrationSerializer
from .models import Tenant

User = get_user_model()

@extend_schema_view(
    create=extend_schema(
        summary="Register a new tenant",
        description="Create a new user with the 'tenant' role.",
        responses={201: TenantRegistrationSerializer},
        request=TenantRegistrationSerializer,
        tags=['tenant management']
    ),
    list=extend_schema(
        summary="List all tenant",
        description="Retrieve a list of all registered tenants under the authenticated landlord.",
        responses={200: TenantRegistrationSerializer(many=True)},
        tags=['tenant management']
    ),
    retrieve=extend_schema(
        summary="Retrieve a tenant",
        description="Retrieve details of a specific tenant by UUID.",
        responses={200: TenantRegistrationSerializer},
        tags=['tenant management']
    ),
    update=extend_schema(
        summary="Update a tenant",
        description="Update details of a specific tenant.",
        responses={200: TenantRegistrationSerializer},
        tags=['tenant management']
    ),
    partial_update=extend_schema(
        summary="Update a tenant partially",
        description="Update details of a specific tenant partially.",
        responses={200: TenantRegistrationSerializer},
        tags=['tenant management']
    ),
    destroy=extend_schema(
        summary="Delete a tenantd",
        description="Delete a specific tenant.",
        responses={204: None},
        tags=['tenant management']
    ),
)
class TenantRegistrationViewSet(viewsets.ModelViewSet):
    """
    Viewset for registering tenants.
    """

    serializer_class = TenantRegistrationSerializer
    permission_classes = [IsAuthenticated, IsLandLord]

    # filtering, searching and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter

    ]
    filterset_fields = ['username','email', 'first_name', 'last_name']
    search_fields = ['email', 'first_name', 'last_name', 'username']
    ordering_fields = ['date_joined', 'username']
    ordering = ['date_joined']
    
    def get_queryset(self):
        return User.objects.filter(
            tenant__landlord=self.request.user
        )
    
    def perform_create(self, serializer):
        # create a tenant profile
        tenant = serializer.save()
        Tenant.objects.create(
            tenant=tenant,
            landlord=self.request.user
        )
        
    