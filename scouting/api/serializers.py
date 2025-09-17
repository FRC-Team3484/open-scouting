from rest_framework import serializers
from main.models import Data, Event, Pit


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        exclude = ["user_created", "username_created", "team_number_created", "account"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ["user_created"]


class PitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pit
        fields = "__all__"


class TeamNumberSerializer(serializers.Serializer):
    team_number = serializers.IntegerField()
