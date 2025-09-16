from rest_framework import serializers
from apps.attributes.api.serializers.attribute_serializers import AttributeGetSerializers
from apps.tasks.models import Task

# Hace referencia al serializador de tareas 
class TasksSerializers(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title', 'description', 'status_task')
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


    #def validate(self, data):
    #    try:

    #        return data
    #    except Exception as e:
    #        raise e

#Hace referencia al serilizador de listado de tareas
class TasksGetSerializers(serializers.ModelSerializer):
    status_task = AttributeGetSerializers()
    class Meta:
        model = Task
        fields = ('id','title', 'description', 'user','status_task')



