# django

## How to setup project?

first clone the repo
```
cd django
pip install virtualenv
virtualenv env
source env/lib/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```


To run the tests use the following command
```
python manage.py test
```