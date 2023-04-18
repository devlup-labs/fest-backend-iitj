from django.urls import path
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('auth/token/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
