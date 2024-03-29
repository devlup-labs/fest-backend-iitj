from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MyObtainTokenPairView, UserProfileViewSet, UserDetailAPI, UserProfileDetailsView, RegisterUserAPIView, CookieTokenRefreshView, PreRegistrationAPIView, GoogleRegisterView, GoogleLoginView, GoogleRegisterViewApp, GoogleLoginViewApp, LogoutView

router = routers.DefaultRouter()
router.register(r'pre-register', PreRegistrationAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('register/google/', GoogleRegisterView.as_view(), name='google-register'),
    path('register/google/app/', GoogleRegisterViewApp.as_view(), name='google-register-app'),
    path('login/google/', GoogleLoginView.as_view(), name='google-login'),
    path('login/google/app/', GoogleLoginViewApp.as_view(), name='google-login-app'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileViewSet.as_view(), name='profile'),
    path('refresh/', CookieTokenRefreshView.as_view(), name='refresh'),
    path('user-details/', UserDetailAPI.as_view()),
    path('user-profile-details/', UserProfileDetailsView.as_view()),
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
