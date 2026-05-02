import os
import django

# Apne project ki settings ko set karein
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pharmacy_project.settings')
django.setup()

from django.contrib.auth.models import User

# Check karein agar 'admin' naam ka user pehle se nahi hai
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("Superuser 'admin' created successfully!")
else:
    print("Superuser already exists.")