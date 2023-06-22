from rest_framework import serializers

from .models import Sponsor


class SponsorSerializer(serializers.Serializer):
    class Meta:
        model = Sponsor
        fields = ('sponsor_image', 'sponsor_name', 'sponsor_link', 'is_old')
