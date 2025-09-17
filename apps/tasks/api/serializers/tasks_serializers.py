from apps.base.extensions.general_serializers import EagerLoadingMixin
from apps.users.api.serializers.users_serializers import UserListUniqueSerializer
from rest_framework import serializers
from apps.attributes.api.serializers.attribute_serializers import AttributeGetSerializers
from apps.tasks.models import Task

# Hace referencia al serializador de tareas 
class TasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status_task')
        read_only_fields = ['user']
        extra_kwargs = {
            'title': {
                "required": True,
                "error_messages": {
                    "required": "El titulo es requerido",
                    "null": "El titulo no puede ser nulo",
                }
            },
             'description': {
                "required": True,
                "error_messages": {
                    "required": "La descripcion es requerida",
                    "null": "La descripcion no puede ser nulo",
                }
            },
            'status_task': {
                "required": True,
                "error_messages": {
                    "required": "El estado es requerida",
                    "null": "El estado no puede ser nulo",
                }
            }
        }


    def update(self, instance, validated_data):
        try:
            # Validación: solo el dueño puede actualizar
            request = self.context.get('request') 
            if request and instance.user != request.user:
                raise Exception("No tienes permisos para actualizar esta tarea.")

            # Actualizamos los campos
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance
        except Exception as e:
            raise e


#Hace referencia al serilizador de listado de tareas
class TasksGetSerializers(serializers.ModelSerializer,EagerLoadingMixin):
    status_task = AttributeGetSerializers()
    user = UserListUniqueSerializer()
    class Meta:
        model = Task
        fields = ('id','title', 'description','create_date', 'user','status_task')



