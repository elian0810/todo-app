from rest_framework.routers import DefaultRouter
from apps.tasks.api.tasks_api import TaskViewSet

router = DefaultRouter()

router.register(r'', TaskViewSet, basename='tasks') # Ruta de tareas
urlpatterns = router.urls

