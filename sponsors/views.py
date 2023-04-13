from rest_framework import permissions
from .models import Sponsor
from .serializers import SponsorSerializer
from rest_framework.generics import ListAPIView
# from django.db.models import Prefetch
from rest_framework.response import Response


class SponsorView(ListAPIView):
    def get(self, request):
        permission_classes = [permissions.AllowAny]
        # serializer_class = SponsorSerializer
        model = Sponsor
        queryset = Sponsor.objects.all()
        serializer = SponsorSerializer(queryset, many=True)
        return Response({"data": serializer.data})

