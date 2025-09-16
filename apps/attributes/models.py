from django.db import models

# Create your models here.

# Hace referencia al modelo de paramtros 
class Parameter(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(help_text="Hace referencia al nombre del parametro.", null=False, blank= False, max_length=255)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'parameters'
        default_permissions=()


# Hace referencia al modelo atributos
class Attribute(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(help_text="Hace referencia al nombre del parametro.", null=False, blank= False, max_length=255)
    paramter = models.ForeignKey(Parameter,on_delete=models.CASCADE, help_text="Hace referencia al id del paramtro.", null=True, blank=True)
    status = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True, null=True)
    update_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'attributes'
        default_permissions=()




