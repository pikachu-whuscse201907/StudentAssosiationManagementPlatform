rd people\migrations\ /s /q
rd media\org_logo\ /s /q
rd media\user_logo\ /s /q
rd media\activ_photo\ /s /q
del db.sqlite3
python manage.py makemigrations people
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
