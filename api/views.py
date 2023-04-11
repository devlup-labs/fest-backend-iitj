from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *


class VerticlesViewSet(viewsets.ModelViewSet):
    queryset = Verticles.objects.all()
    serializer_class = VerticlesSerializer
    # permission_classes = [permissions.IsAuthenticated]


class CoreTeamViewSet(viewsets.ModelViewSet):
    queryset = CoreTeam.objects.all()
    serializer_class = CoreTeamSerializer
    # permission_classes = [permissions.IsAuthenticated]
