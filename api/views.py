from rest_framework import permissions
from .models import Vertical, CoreMember
from .serializers import AllVerticalSerializer
from django.db.models import Prefetch
from rest_framework.generics import ListAPIView


class AllVerticalViewSet(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AllVerticalSerializer
    model = Vertical
    queryset = Vertical.objects.prefetch_related(
        Prefetch('new_position', queryset=CoreMember.objects.all(), to_attr='core_members')
    ).order_by('rank')
