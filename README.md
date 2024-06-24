# Multi_DB

# Multi_DB Project

This project demonstrates the use of multiple databases with Django. Below are the steps to set up and run the project.

## Step 1: Create a Virtual Environment

```sh
STEP 1

python -m venv myenv

STEP 2

# Windows
myenv\Scripts\activate
# macOS and Linux
source myenv/bin/activate

STEP 3

pip install -r requirements.txt


STEP 4

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'techto',
        'USER': 'pradheep',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'testing',
        'USERNAME': 'groot',
        'PASSWORD': 'Prad@246',
    }
}

User_login Project
python manage.py runserver

Postgres_user
python manage.py runserver 8080


open a index.html in browser



API URL
http://127.0.0.1:8000/api/schema/swagger-ui/#/
