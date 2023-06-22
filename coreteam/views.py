from django.db.models import Prefetch
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import CoreMember, Vertical
from .serializers import AllVerticalSerializer


class AllVerticalsAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AllVerticalSerializer
    model = Vertical
    queryset = Vertical.objects.prefetch_related(
        Prefetch('new_position', queryset=CoreMember.objects.all(),
                 to_attr='core_members')
    ).order_by('rank')
