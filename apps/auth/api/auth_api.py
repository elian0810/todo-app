from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.auth.api.serializers.auth_serializers import CustomTokenObtainPairSerializer, UserTokenSerializer
from apps.base.helpers.format_response import FormatResponse
from django.contrib.auth import authenticate
from apps.base.helpers.custom_exception import CustomException
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
   
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email','')
            password = request.data.get('password','')
            user = authenticate(
                email = email,
                password = password,
            )
            if user:
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():
                    user_serializer = UserTokenSerializer(user)
                    # Verificamos si el usuario esta activo o esta desactivado
                    if(user.is_active is False):
                        CustomException.throw("El usuario aún tiene una cuenta activa")
                    if(user.status is False):
                        CustomException.throw("El usuario se encuentra suspendido")
                    # Obtenemos el menu del rol
                    return FormatResponse.successful(message="Inicio de sesión exitoso",
                        data={  
                              'user': user_serializer.data,
                              'token': login_serializer.validated_data.get('access'),
                              'refresh-token': login_serializer.validated_data.get('refresh'),
                              'access_token_lifetime' : settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                              'refresh_token_lifetime' : settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                              }, status= status.HTTP_200_OK)
                CustomException.throw("Ha ocurrido un error con el usuario proporcionado")
            CustomException.throw("Credenciales inválidas")

        except Exception as e:
            return FormatResponse.failed(e)

class Logout(GenericAPIView):
    permission_classes= (IsAuthenticated,)
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            if user is not None:
                RefreshToken.for_user(user)
                return FormatResponse.successful(message="Sesión cerrada con éxito")
            CustomException.throw("No existe el usuario")
        except Exception as e:
            return FormatResponse.failed(e)