from apps.base.general_querys import CDB
from apps.attributes.models import Attribute
from apps.attributes.enums.parameter_enums import ParametersEnum

class AttributeSeeder:

     def __init__(self):
          print("Seeding AttributeSeeder...")
          # Group.objects.all().delete()
          CDB.restart_sequence([Attribute])
          #======================================================================================================
          #====================== Estados =======================================================
          Attribute.objects.create(name='Activo', parameter_id=ParametersEnum.STATUS_TASK.value)# nit de la empresa 
          Attribute.objects.create(name='Inactivo', parameter_id=ParametersEnum.STATUS_TASK.value)# nit de la empresa 
          Attribute.objects.create(name='Cancelado', parameter_id=ParametersEnum.STATUS_TASK.value)# nit de la empresa 

          print("AttributeSeeder Excueted!")