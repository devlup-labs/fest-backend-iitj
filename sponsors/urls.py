from django.urls import path
from .views import SponsorView


app_name = "sponsors"


urlpatterns = [
    path('sponsors/', SponsorView.as_view()),
]
