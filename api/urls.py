from django.urls import path, include
from .views import AllVerticalViewSet
from rest_framework import routers

router = routers.DefaultRouter()
# router.register('vertical', AllVerticalViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vertical/', AllVerticalViewSet.as_view(), name='vertical'),
]
