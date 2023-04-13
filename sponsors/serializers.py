from rest_framework import serializers
from .models import Sponsor


class SponsorSerializer(serializers.Serializer):
    sponsor_image = serializers.ImageField()
    sponsor_name = serializers.CharField(max_length=10)
    sponsor_link = serializers.URLField(max_length=255)
    is_old = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Sponsor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.body = validated_data.get('body', instance.body)
        instance.author_id = validated_data.get('author_id', instance.author_id)

        instance.save()
        return instance
