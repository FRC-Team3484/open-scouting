from rest_framework import serializers
from main.models import Data


class ScoutingReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"  # or pick specific fields
