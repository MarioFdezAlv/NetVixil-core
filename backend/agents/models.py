from django.db import models
from accounts.models import User


class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agents")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField()
    mac_address = models.CharField(max_length=17, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"


class NetworkData(models.Model):
    agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="network_data"
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField()
    mac = models.CharField(max_length=17, blank=True)
    hostname = models.CharField(max_length=100, blank=True)
    manufacturer = models.CharField(max_length=100, blank=True)
    online = models.BooleanField(default=True)
    ports = models.JSONField(default=list, blank=True)
    os = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.agent.name} - {self.ip} @ {self.timestamp}"
