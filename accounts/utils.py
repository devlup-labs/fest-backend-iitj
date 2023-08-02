from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_registration_code(name, lastRegCode):
    return f"{name[:3].upper()}-{lastRegCode+3155}"
