from rest_framework import serializers

from .models import CoreMember, Vertical


class CoreMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreMember
        fields = '__all__'


class AllVerticalSerializer(serializers.ModelSerializer):
    coremembers = CoreMemberSerializer(
        source='core_members',
        many=True,
        read_only=True
    )

    class Meta:
        model = Vertical
        fields = ('name', 'rank', 'coremembers')
