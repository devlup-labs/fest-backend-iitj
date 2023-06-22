from django.urls import path

from .views import AllVerticalsAPIView

urlpatterns = [
    path('', AllVerticalsAPIView.as_view(), name='coreteam'),
]
