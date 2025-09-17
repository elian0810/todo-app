from rest_framework.routers import DefaultRouter
from apps.attributes.api.attribute_api import AttributeViewSet

router = DefaultRouter()

router.register(r'', AttributeViewSet, basename='attributes') #ruta de Attributos


urlpatterns = router.urls