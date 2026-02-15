echo "Installing dependencies..."
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Creating admin user..."
python manage.py shell < registration/create_admin.py


echo "Collecting static files..."
python manage.py collectstatic --noinput

