

# echo "Installing dependencies..."
# pip install -r requirements.txt

# echo "Running migrations..."
# python manage.py migrate

# echo "Collecting static files..."
# python manage.py collectstatic --noinput






# echo "from django.contrib.auth import get_user_model;
# User = get_user_model();
# User.objects.filter(username='admin').exists() or
# User.objects.create_superuser('admin', 'surbhidharvan@gmail.com', 'admin123')" | python manage.py shell

#!/usr/bin/env bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

