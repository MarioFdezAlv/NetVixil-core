from rest_framework import serializers
from .models import Agent, NetworkData


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = [
            "id",
            "user",
            "name",
            "description",
            "ip_address",
            "mac_address",
            "last_seen",
            "active",
        ]
        read_only_fields = ["user", "last_seen"]


class NetworkDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkData
        fields = [
            "id",
            "agent",
            "timestamp",
            "ip",
            "mac",
            "hostname",
            "manufacturer",
            "online",
            "ports",
            "os",
        ]
        read_only_fields = ["timestamp"]
