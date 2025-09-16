from apps.base.extensions.general_serializers import EagerLoadingMixin
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from apps.users.models import User

class PersonWithUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este correo ya está registrado" 
            )
        ],
        error_messages={
            "required": "El correo electrónico es obligatorio",
            "invalid": "El correo electrónico no es válido",
        }
    )
    class Meta:
        model = User
        fields = ['email', 'password', 'name', 'last_name', 'image']  # solo los necesarios
        extra_kwargs = {
            'password': {
                'required': True,
                'write_only': True,
                'error_messages': {
                    'required': 'La contraseña es obligatoria'
                }
            },
            'name': {
                'required': True,
                'error_messages': {
                    'required': 'El nombre es obligatorio'
                }
            },
            'last_name': {
                'required': True,
                'error_messages': {
                    'required': 'El apellido es obligatorio'
                }
            },
        }

    def create(self, validated_data):
        try:
            password = validated_data.pop('password')
            user = User(
                username=validated_data['email'],
                email=validated_data['email'],
                name=validated_data['name'],
                last_name=validated_data['last_name'],
                status=True,
                is_active=True,
                image=validated_data.get('image', None)
            )
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise e


    def update(self, instance, validated_data):
        try:
            # Actualizamos los datos del usuario directamente
            instance.email = validated_data.get('email', instance.email)
            instance.username = validated_data.get('email', instance.username)
            instance.name = validated_data.get('name', instance.name)
            instance.last_name = validated_data.get('last_name', instance.last_name)
   
            # Si viene password, actualizarla correctamente
            password = validated_data.get('password', None)
            if password:
                instance.set_password(password)
   
            if 'image' in validated_data:
                instance.image = validated_data['image']
   
            instance.save()
            return instance
        except Exception as e:
            raise e


class UserListUniqueSerializer(serializers.ModelSerializer,EagerLoadingMixin):
    class Meta:
        model = User
        fields = '__all__'



