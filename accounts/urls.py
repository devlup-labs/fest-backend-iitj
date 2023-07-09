from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MyObtainTokenPairView, UserProfileViewSet, UserViewSet

urlpatterns = [
    path('signup/', UserViewSet.as_view(), name='signup'),
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('profile/', UserProfileViewSet.as_view(), name='profile'),
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
