from django.core.management.base import BaseCommand, CommandError
from apps.attributes.seeders.attributes_seeder import AttributeSeeder
from apps.attributes.seeders.parameters_seeder import ParameterSeeder
from apps.users.seeders.users_seeder import UsersSeeder

class Command(BaseCommand):
    """Exec command $ python manage.py db_seed"""
    help='Corre los seeders necesarios para el funcionamiento de la aplciación'

    def add_arguments(self, parser):
        parser.add_argument('--class', nargs='+', type=str)


    def handle(self, *args, **options):

       try:
            class_seeder = options.get('class', None)
            if class_seeder is not None:
                globals()[class_seeder[0]]()
                pass
            else:
                #seeder de parametros y atributos
                ParameterSeeder()
                AttributeSeeder()
                UsersSeeder()
            self.stdout.write("Executed seeder ", ending='\n')
       except KeyError:
        print("El seeder especificado no existe")
       except Exception as e:
        raise e
        print("Ha ocurrido un error no previsto", type(e).__name__ )