from django.contrib.auth import login
from djoser.serializers import UserSerializer
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema
from knox.auth import TokenAuthentication
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework.request import Request


class MyAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = TokenAuthentication
    name = "Token Authentication"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Value should be formatted: `Token <key>`"
        }


class LoginView(KnoxLoginView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=AuthTokenSerializer,
        responses={200: UserSerializer}
    )
    def post(self, request: Request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format)
