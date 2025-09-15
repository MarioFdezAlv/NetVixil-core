from rest_framework import generics, permissions
from .models import Agent, NetworkData
from .serializers import AgentSerializer, NetworkDataSerializer


class AgentListCreateView(generics.ListCreateAPIView):
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Agent.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NetworkDataListCreateView(generics.ListCreateAPIView):
    serializer_class = NetworkDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return NetworkData.objects.filter(agent__user=self.request.user)

    def perform_create(self, serializer):
        agent_id = self.request.data.get("agent")
        agent = Agent.objects.get(id=agent_id, user=self.request.user)
        serializer.save(agent=agent)
