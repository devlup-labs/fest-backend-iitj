import datetime
from django.conf import settings
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.contrib.auth import get_user_model, authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, status, viewsets, exceptions, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserProfile, PreRegistration, BlacklistedEmail
from .serializers import MyTokenObtainPairSerializer, UserProfileSerializer, UserSerializer, RegisterSerializer, CookieTokenRefreshSerializer, PreRegistrationSerializer
from .utils import get_tokens_for_user, google_get_access_token, google_get_user_info

User = get_user_model()


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class PreRegistrationAPIView(viewsets.ModelViewSet):
    queryset = PreRegistration.objects.all()
    serializer_class = PreRegistrationSerializer


class UserProfileViewSet(APIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request):
        profile = UserProfile.objects.create(user_id=request.data['user'])
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            profile.user.profile_complete = True
            profile.user.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create(
                username=request.data['email'],
                email=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )

            user.set_password(request.data['password'])

            user.save()
        except Exception:
            return Response({"Error": "User already exists, try to sign-in!!"}, status=status.HTTP_409_CONFLICT)

        response = Response()

        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isProfileComplete',
                    value=user.profile_complete,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isGoogle',
                    value=user.is_google,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )

                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                return Response({"Error": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Error": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        if UserProfile.objects.filter(user=user).exists():
            userprofile = UserProfile.objects.get(user=user)
            userserializer = UserSerializer(user)
            userprofileserializer = UserProfileSerializer(userprofile)

            return Response({"user": userserializer.data, "userprofile": userprofileserializer.data})
        else:
            return Response({"Error": "User profile is not complete!!"}, status=status.HTTP_404_NOT_FOUND)


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if request.COOKIES.get("refresh"):
            response.set_cookie(
                key='access',
                value=response.data["access"],
                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                secure=True,
                domain="",
                httponly=True,
                samesite='Lax'
            )

        return super().finalize_response(request, response, *args, **kwargs)


class GoogleRegisterView(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login'

        if error or not code:
            params = urlencode({'Error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_BACKEND_URL}/accounts/login/google/'

        try:
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        except Exception:
            params = urlencode({'Error': "Failed to obtain access token from Google."})
            return redirect(f'{login_url}?{params}')

        try:
            user_data = google_get_user_info(access_token=access_token)
        except Exception:
            params = urlencode({'Error': "Failed to obtain user info from Google."})
            return redirect(f'{login_url}?{params}')

        if BlacklistedEmail.objects.filter(email=user_data["email"]).exists():
            params = urlencode({'Error': "This email is blacklisted"})
            return redirect(f'{login_url}?{params}')

        try:
            user = User.objects.create(
                username=user_data['email'],
                email=user_data['email'],
                first_name=user_data.get('given_name', ''),
                last_name=user_data.get('family_name', ''),
                google_picture=user_data.get('picture', ''),
                is_google=True,
            )
            user.set_password('google')

            if user_data['email'][-10:] == "iitj.ac.in":
                user.iitj = True

            user.save()
        except Exception:
            params = urlencode({'Error': "User already exists, try to sign-in!"})
            return redirect(f'{login_url}?{params}')

        response = Response(status=302)
        user = authenticate(username=user_data['email'], password='google')
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isProfileComplete',
                    value=user.profile_complete,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isGoogle',
                    value=user.is_google,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain="",
                    httponly=False,
                    samesite='Lax'
                )
                if user.profile_complete:
                    response['Location'] = f'{settings.BASE_FRONTEND_URL}'  # homepage url

                else:
                    response['Location'] = f'{settings.BASE_FRONTEND_URL}/profile'  # complete profile url

                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                params = urlencode({'Error': "This account is not active!!"})
                return redirect(f'{login_url}?{params}')
        else:
            params = urlencode({'Error': "Invalid username or password!!"})
            return redirect(f'{login_url}?{params}')


class GoogleRegisterViewApp(APIView):
    def post(self, request, format=None):
        secret = settings.APP_SECRET
        incoming_secret = request.headers.get('X-App')

        if secret != incoming_secret:
            return Response(data={"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        if BlacklistedEmail.objects.filter(email=data.get("email")).exists():
            return Response(data={"message": "This email is blacklisted"}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.create(
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data.get('email'),
                username=data.get('email'),
                google_picture=data.get('picture', ''),
                is_google=True
            )
        except Exception:
            return Response(data={"message": "User Already Exists"}, status=status.HTTP_409_CONFLICT)

        user.set_password('google')

        if data.get('email')[-10:] == "iitj.ac.in":
            user.iitj = True

        user.save()

        user = authenticate(username=data.get('email'), password='google')

        if user is None:
            return Response(data={"message": "Username or Password Invalid"}, status=status.HTTP_404_NOT_FOUND)

        data = get_tokens_for_user(user)

        res = Response(
            data={
                "message": "Registration Successful",
                "access": data["access"],
                "refresh": data["refresh"]
            },
            status=status.HTTP_201_CREATED
        )

        return res


class GoogleLoginView(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = f'{settings.BASE_FRONTEND_URL}/login/'

        if error or not code:
            params = urlencode({'Error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = f'{settings.BASE_BACKEND_URL}/accounts/login/google/'

        try:
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        except Exception:
            params = urlencode({'Error': "Failed to obtain access token from Google."})
            return redirect(f'{login_url}?{params}')

        try:
            user_data = google_get_user_info(access_token=access_token)
        except Exception:
            params = urlencode({'Error': "Failed to obtain user info from Google."})
            return redirect(f'{login_url}?{params}')

        if BlacklistedEmail.objects.filter(email=user_data["email"]).exists():
            params = urlencode({'Error': "This email is blacklisted"})
            return redirect(f'{login_url}?{params}')

        response = Response(status=302)

        if User.objects.filter(email=user_data['email']).exists():
            if User.objects.get(email=user_data['email']).is_google:
                user = authenticate(username=user_data['email'], password='google')
                if user is not None:
                    if user.is_active:
                        data = get_tokens_for_user(user)
                        response.set_cookie(
                            key='access',
                            value=data["access"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain="",
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='refresh',
                            value=data["refresh"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain="",
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='LoggedIn',
                            value=True,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain="",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isProfileComplete',
                            value=user.profile_complete,
                            expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain="",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isGoogle',
                            value=user.is_google,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain="",
                            httponly=False,
                            samesite='Lax'
                        )

                        if user.profile_complete:
                            response['Location'] = f'{settings.BASE_FRONTEND_URL}'  # homepage url
                        else:
                            response['Location'] = f'{settings.BASE_FRONTEND_URL}/profile'  # complete profile url

                        response.data = {"Success": "Login successfull", "data": data}
                        return response
                    else:
                        params = urlencode({'Error': "This account is not active!!"})
                        return redirect(f'{login_url}?{params}')
                else:
                    params = urlencode({'Error': "Please Signup first!!"})
                    return redirect(f'{login_url}?{params}')
            else:
                params = urlencode({'Error': "You signed up using email & password!!"})
                return redirect(f'{login_url}?{params}')
        else:
            params = urlencode({'Error': "Please Signup first!!"})
            return redirect(f'{login_url}?{params}')


class GoogleLoginViewApp(APIView):
    def post(self, request, format=None):
        secret = settings.APP_SECRET
        incoming_secret = request.headers.get('X-App')

        if secret != incoming_secret:
            return Response(data={"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        if BlacklistedEmail.objects.filter(email=data.get('email')).exists():
            return Response(data={"message": "This email is blacklisted"}, status=status.HTTP_403_FORBIDDEN)

        if User.objects.filter(email=data.get('email')).exists():
            user = User.objects.get(email=data.get('email'))

            if user.is_google:
                user = authenticate(username=data.get('email'), password='google')

                if user is None:
                    return Response(data={"message": "Username or Password Invalid"}, status=status.HTTP_404_NOT_FOUND)

                data = get_tokens_for_user(user)

                res = Response(
                    data={
                        "message": "Logged In Successfully",
                        "access": data["access"],
                        "refresh": data["refresh"]
                    },
                    status=status.HTTP_200_OK
                )

                return res
            else:
                return Response(data={"message": "You signed up using email and password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={"message": "You need to sign up before you can login"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refreshToken = request.COOKIES.get('refresh')
            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie('access', domain="")
            res.delete_cookie('refresh', domain="")
            res.delete_cookie('LoggedIn', domain="")
            res.delete_cookie("isProfileComplete", domain="")
            res.delete_cookie("isGoogle", domain="")

            return res
        except Exception:
            raise exceptions.ParseError("Invalid token")
