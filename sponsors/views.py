from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import Sponsor
from .serializers import SponsorSerializer


class SponsorView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SponsorSerializer
    model = Sponsor
    queryset = Sponsor.objects.all()
