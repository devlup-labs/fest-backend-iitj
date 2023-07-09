from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, UserProfile
from .serializers import MyTokenObtainPairSerializer, UserProfileSerializer, UserSerializer


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class UserProfileViewSet(APIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request):
        profile = UserProfile.objects.create(user_id=request.data['user'])
        serializer = UserProfileSerializer(profile, data=request.data)
        # print(serializer.user)
        # print(request.data.user)
        if serializer.is_valid():
            serializer.save()
            profile.user.profile_complete = True
            profile.user.save()
            # print(profile.user.profile_complete)
            return Response(serializer.data)
        return Response(serializer.errors)

class UserViewSet(APIView): 
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    