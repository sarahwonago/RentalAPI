from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsLandLord

from .serializers import TenantRegistrationSerializer
from .models import Tenant

User = get_user_model()

class TenantRegistrationViewSet(viewsets.ModelViewSet):
    """
    Viewset for registering tenants.
    """

    serializer_class = TenantRegistrationSerializer
    permission_classes = [IsAuthenticated, IsLandLord]
    
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
        
    

