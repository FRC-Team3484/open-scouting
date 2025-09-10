from rest_framework.permissions import AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework import viewsets

from main.models import Data
from .serializers import ScoutingReportSerializer


class ScoutingReportViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = ScoutingReportSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            return [AllowAny()]  # anyone can discover endpoints
        return [HasAPIKey()]  # API key required for everything else
