from rest_framework import viewsets
from django.db.models import Q,  F, Value, CharField
from django.db.models.functions import Concat
from django.db import  transaction
from rest_framework.permissions import IsAuthenticated
from apps.base.custom_pagination.custom_pagination import BasicPagination
from apps.base.helpers.custom_exception import CustomException
from apps.base.helpers.format_response import FormatResponse
from apps.base.utils import formatErrors, setActorRequest
from apps.users.api.serializers.users_serializers import PersonWithUserSerializer, UserListUniqueSerializer
from apps.users.models import User

class UsersViewSet(viewsets.GenericViewSet):
    #llamamos a nuestro modelo
    model = User
    #aplicamos la paginacion
    pagination_class = BasicPagination
    #pasamos nuestro serilizador
    serializer_class = PersonWithUserSerializer
    # Personalizamos nuestro list_serializer_class segun nuestro serlizador
    list_serializer_class = UserListUniqueSerializer
    #imponemos caracteriticas sobre nuestros queryset
    queryset = User.objects.filter(status=True)
    #Verificamos el sitemea de aut. por toekn bearer
    # permission_classes = (IsAuthenticated,)
   
   
    def create(self, request, *args, **kwargs):
        """
        Creacion de un usuario generico del sistema

        - params:
        name => Nombre del usuario
        """
        try:
            with transaction.atomic():
                # ===================================================
                # Registramos en el modelo usuario y persona
                serializer = PersonWithUserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    CustomException.throw(formatErrors(serializer.errors))
                               
            return FormatResponse.successful(message="Usuario creado con éxito", data=serializer.data)
        except Exception as e:
            return FormatResponse.failed(e)

       
    def update(self, request,pk=None):

        """
        Funcion que actuliza el objeto recibiendo
        el pk de ese mismo por medio de la ruta
        """
        try:
            with transaction.atomic():
                instance = User.objects.filter(pk=pk, status=True).first()
                if not instance:
                    CustomException.throw("El usuario con el id enviado no existe en el sistema.")

                serializer = PersonWithUserSerializer(instance, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    CustomException.throw(formatErrors(serializer.errors))

            return FormatResponse.successful(message="Usuario actualizado con éxito", data=serializer.data)
        except Exception as e:
            return FormatResponse.failed(e)

   
   
    def destroy(self, request, pk=None):
        """
        Eliminación de un usuario
        """
        try:
            # Obtenemos a el usuario autenticado
            with transaction.atomic():

                # Obtenemos la entidad person
                user = User.objects.filter(pk=pk,status=True).first()
                if user is None: CustomException.throw("El usuario especificado no existe")
               
               
                user.status=False;
                # Actualizamos el status tambien en la entidad User
                user.status=False;
                user.is_active=False;
                user.save();
             
            return FormatResponse.successful(message="Usuario eliminado con éxito")
        except Exception as e:
            return FormatResponse.failed(e)


    def list(self, request, *args, **kwargs):
        """
        Listado de usuarios

        - params:
          limit => Limite de registros
          page => Página actual del sistema
        """
        try:
            #Variable que hace referencia al input
            search = self.request.query_params.get('search', '')
            #fltros a realizar en la consulta de listado
            rol_id = self.request.query_params.get('rol_id',None)
            #pasamos el modelo al cual le aplicamos los filtros
            users = User.objects.filter(status=True)
   
            # Obtenemos a el usuario autenticado
            users = users.order_by('-id').all()

            #=============================================================
            #Pasampos las columans permitas a filtrar en nuestro input
            if search:
                users = users.annotate(
                    full_name=Concat('name', Value(' '), 'last_name', output_field=CharField()),
                ).filter(
                    Q(name__icontains=search)
                )
 
            # Realizamos la precarga de las relaciones
            users = self.list_serializer_class().setup_eager_loading(users)
           
            page = self.paginate_queryset(users)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.list_serializer_class(page, many=True).data)
            else:
                serializer = self.list_serializer_class(users, many=True)
         
            return FormatResponse.successful(message="Listado de usuarios con éxito", data=serializer.data)
        except Exception as e:
            return FormatResponse.failed(e)
   


