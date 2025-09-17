from rest_framework import serializers
from main.models import Data, Event, Pit


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class PitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pit
        fields = "__all__"


class TeamNumberSerializer(serializers.Serializer):
    team_number = serializers.IntegerField()
