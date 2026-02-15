from django.contrib.auth import get_user_model
import os

User = get_user_model()

username = os.getenv("ADMIN_USERNAME", "admin")
email = os.getenv("ADMIN_EMAIL", "surbhidharvan@gmail.com")
password = os.getenv("ADMIN_PASSWORD", "Surbhi@1234")

if not User.objects.filter(username=username).exists():
    print("Creating admin user...")
    User.objects.create_superuser(username, email, password)
else:
    print("Admin user already exists.")
