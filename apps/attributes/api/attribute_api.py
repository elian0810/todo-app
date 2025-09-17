from apps.attributes.api.serializers.attribute_serializers import AttributeGetSerializers
from apps.attributes.models import Attribute
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.base.custom_pagination.custom_pagination import BasicPagination
from apps.base.helpers.format_response import FormatResponse


class AttributeViewSet(viewsets.GenericViewSet):
    #llamamos a nuestro modelo 
    model = Attribute
    #aplicamos la paginacion 
    pagination_class = BasicPagination
    #pasamos nuestro serilizador 
    serializer_class = AttributeGetSerializers
    # Personalizamos nuestro list_serializer_class segun nuestro serlizador
    list_serializer_class = AttributeGetSerializers
    #imponemos caracteriticas sobre nuestros queryset
    queryset = Attribute.objects.filter(status=True)
    #Verificamos el sitemea de aut. por toekn bearer
    permission_classes = (IsAuthenticated,)
    
    def list(self, request, *args, **kwargs):
        """
        Listado de Atributos de un usuario en sesión

        - params:
          limit => Limite de registros 
          page => Página actual del sistema 
        """   
        try:
            #fltros a realizar en la consulta de listado 
            parameter_id = self.request.query_params.get('parameter_id', None) 
            include_ids = self.request.query_params.get('include_ids', None) 
           #pasamos el modelo al cual le aplicamos los filtros 
            attribute = Attribute.objects.filter( status=True)
            # Filtramos por el id 
            if include_ids:
                include_ids = list(map(int, include_ids.strip("'").split(',')))
                attribute = attribute.filter(id__in=include_ids)    

            if parameter_id :
                attribute = attribute.filter(parameter_id=parameter_id)    
            # Obtenemos a el usuario autenticado
            user = self.request.user
            attribute = attribute.order_by('-id').all()
            # Realizamos la precarga de las relaciones
            attribute = self.serializer_class().setup_eager_loading(attribute)
            
            page = self.paginate_queryset(attribute)
            if page is not None:
                serializer = self.get_paginated_response(
                    self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(attribute, many=True)

            return FormatResponse.successful(message="Listado de attributos con éxito", data=serializer.data)
        except Exception as e:
            return FormatResponse.failed(e)