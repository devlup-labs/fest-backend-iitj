from rest_framework import serializers
# from .models import Sponsor


class SponsorSerializer(serializers.Serializer):
    sponsor_image = serializers.ImageField()
    sponsor_name = serializers.CharField(max_length=10)
    sponsor_link = serializers.URLField(max_length=255)
    is_old = serializers.BooleanField(default=False)
