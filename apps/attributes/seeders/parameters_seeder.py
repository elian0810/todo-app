from apps.base.general_querys import CDB
from apps.attributes.models import Parameter        
class ParameterSeeder:

     def __init__(self):
          print("Seeding ParameterSeeder...")
          # Group.objects.all().delete()
          CDB.restart_sequence([Parameter])
          #ID 1
          Parameter.objects.create(id= 1, name='Estados de tareas.')
          print("ParameterSeeder Excueted!")