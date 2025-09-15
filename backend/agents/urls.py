from django.urls import path
from .views import AgentListCreateView, NetworkDataListCreateView

urlpatterns = [
    path("agents/", AgentListCreateView.as_view()),
    path("network-data/", NetworkDataListCreateView.as_view()),
]
