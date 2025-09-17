from apps.base.general_querys import CDB
from apps.users.models import User

class UsersSeeder:

    def __init__(self):
        print("Seeding UsersSeeder...")

        # Reinicia la secuencia de IDs para evitar duplicados
        CDB.restart_sequence([User])

        # Limpia los usuarios anteriores (opcional)
        User.objects.all().delete()

        # ========== Usuario administrador ==========
        admin = User(
            username="admin",
            email="admin@example.com",
            name="Administrador",
            last_name="Principal",
            is_staff=True,
            is_active=True,
            status=True
        )
        admin.set_password("admin123")  # contraseña encriptada
        admin.save()

        # ========== Usuario 1 ==========
        user1 = User(
            username="user1",
            email="user1@example.com",
            name="Juan",
            last_name="Pérez",
            is_staff=False,
            is_active=True,
            status=True
        )
        user1.set_password("user123")
        user1.save()

        # ========== Usuario 2 ==========
        user2 = User(
            username="user2",
            email="user2@example.com",
            name="María",
            last_name="Gómez",
            is_staff=False,
            is_active=True,
            status=True
        )
        user2.set_password("user123")
        user2.save()

        print("UsersSeeder executed successfully!")
