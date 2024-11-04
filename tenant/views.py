from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from account.permissions import IsLandLord

from .serializers import TenantSerializer
from .models import Tenant

