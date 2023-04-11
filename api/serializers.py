from rest_framework import serializers
from .models import *


class VerticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verticles
        fields = '__all__'

class CoreTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreTeam
        fields = '__all__'
