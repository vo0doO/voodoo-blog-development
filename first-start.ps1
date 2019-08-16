pip install -r requirements.txt

& "C:\Program Files\PostgreSQL\11\bin\createdb.exe" python_getting_started

python manage.py migrate

python manage.py collectstatic

heroku local