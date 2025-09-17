from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.base.custom_pagination.custom_pagination import BasicPagination
from apps.base.helpers.custom_exception import CustomException
from apps.base.helpers.format_response import FormatResponse
from apps.base.utils import formatErrors
from apps.tasks.api.serializers.tasks_serializers import TasksSerializers, TasksGetSerializers
from apps.tasks.models import Task


# Hace referencia al serializador de tareas
class TaskViewSet(viewsets.GenericViewSet):
    #Modelo al que hace referencia
    model = Task
    # Funcion que pagina la data 
    pagination_class = BasicPagination
    # Serializador para metodos POST y PUT
    serializer_class = TasksSerializers
    # Serializador para meodos GET
    list_serializer_class = TasksGetSerializers
    # Modificamos el Queysert
    queryset = Task.objects.filter(status= True)
    # Validamos si vien el token 
    permission_classes = (IsAuthenticated,)


    def create(self, request, *args, **kwargs):
        try:    
            """
                - Esta funcion realiza la accion de crear las tareas por usuario
            """
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)
            else:
                raise Exception(formatErrors(serializer.errors))
                
            return FormatResponse.successful(message="Tarea creada con exito.", data=request.data)
        except Exception as e:
            return FormatResponse.failed(e)
        

    def update(self, request, *args, **kwargs):
        try:
            """
                - Funcion que realiza la accion de actulizar una tarea
            """
            partial = kwargs.pop('partial', False)
            pk = kwargs.get("pk")

            task = Task.objects.filter(pk=pk).first()
            if not task:
                CustomException.throw("El id enviado no existe en el sistema.")
            #obentemos nuestra instancia
            instance = self.get_object()

            #obtemenos la infromacion de nuetro serilizador y la validamos
            serializer = self.get_serializer_class()(instance, data=request.data, context={'request': request}, partial=True )
            if serializer.is_valid():
                serializer.save(user=request.user)
            else:
                CustomException.throw(formatErrors(serializer.errors))
            
            return FormatResponse.successful(message="Tarea actualizada con exito.", data=request.data)
        except Exception as e:
            return FormatResponse.failed(e)
        


    def destroy(self, request, *args, **kwargs):
        try:
            """
                - Funcion que realiza la accion de inactivar una tarea
            """
            pk = kwargs.get("pk")
            task = Task.objects.filter(pk=pk).first()
            if not task:
                CustomException.throw("El id enviado no existe en el sistema.")
                
            if task.user != request.user:
                CustomException.throw("No tienes permisos para eliminar esta tarea.")

            task_destroy = self.get_object()
            task_destroy_serializer = self.serializer_class(task_destroy)
            task_destroy_serializer.instance.status = False
            task_destroy_serializer.instance.save()
            return FormatResponse.successful(message="Tarea eliminada con exito.", data={})
        except Exception as e:
            return FormatResponse.failed(e)
        

    def list(self, request, *args, **kwargs):
        try:
            user_id = request.user.id if request.user.id else None

            task = Task.objects.filter(status=True)

            if user_id:
                task = task.filter(user_id=user_id)

            task.order_by('-id')

            task = self.list_serializer_class().setup_eager_loading(task)
            page = self.paginate_queryset(task)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.list_serializer_class(page, many=True).data)
            else:
                serializer = self.list_serializer_class(task, many=True)

            return FormatResponse.successful(message="Listado de tareas obtenidas con exito.", data=serializer.data)
        except Exception as e:
            return FormatResponse.failed(e)
        





    