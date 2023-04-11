from django.urls import path, include
from .models import *
from .serializers import *
from .views import *
from rest_framework import routers, serializers, viewsets

router = routers.DefaultRouter()
router.register('verticles', VerticlesViewSet)
router.register('coreteam', CoreTeamViewSet)

urlpatterns = [
    path('', include(router.urls)),
]