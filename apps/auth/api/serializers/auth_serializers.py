from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenRefreshSerializer
from apps.users.models import User

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    pass

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar el rol del usuario en la carga útil del token
        token['role'] = 1
        token['mod'] = 0
        return token
   
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['mod'] = 0  # Agregar el campo "mod" con el valor 0
        return data
   

class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'username', 'email','creation_date','last_update')
   
