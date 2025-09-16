from apps.users.api.users_api import UsersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', UsersViewSet, basename='users') # Ruta de usuarios
urlpatterns = router.urls

