from rest_framework import viewsets

from .serializers import TenantSerializer
from .models import Tenant

class TenantViewSet(viewsets.ModelViewSet):
    """
    Viewset for tenants.
    """
    serializer_class = TenantSerializer

    def get_queryset(self):
        return Tenant.objects.all()
    
