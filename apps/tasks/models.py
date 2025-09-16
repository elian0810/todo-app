from django.db import models
from apps.attributes.models import Attribute
from apps.users.models import User

# Hace referencia al modelo de tareas
class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(help_text="Hace referencia al nombre de la tarea", null=False, blank=False, max_length=255)
    description = models.CharField(help_text="Hace referencia a la descripcion de la tarea", null=True, blank=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Hace referencia al id del usuario.", null=False, blank=False)
    status_task = models.ForeignKey(Attribute,on_delete=models.CASCADE,  help_text="Hace referencia al estado de la tarea.", null=False, blank=False)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'Tasks'
        default_permissions=()

