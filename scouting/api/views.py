from rest_framework import viewsets, permissions
from main.models import Data
from .serializers import ScoutingReportSerializer


class ScoutingReportViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = ScoutingReportSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
