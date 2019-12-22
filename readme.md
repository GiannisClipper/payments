
md projectname

cd projectname

    Create & activate a virtual environment

        ...> python -m venv venv

        ...> venv\scripts\activate

    Install Django and dependencies:

        (venv) ...> pip install django

        (venv) ...> pip install djangorestframework

        (venv) ...> pip install pyjwt

        (venv) ...> pip install django-cors-headers

    Create & run project

        (venv) ...> django-admin startproject apps

        (venv) ...apps> python manage.py runserver

    Install/setup Flake8 for linting:

        (venv) ...> pip install flake8

        (venv) ..apps> touch .flake8

    Install/setup Selenium for functional testing:

        (venv) ...> pip install selenium

        (venv) ...apps> (cp geckodriver.exe .)

    Create application

        (venv) ...apps> python manage.py startapp users

        (add it in INSTALLED_APPS in settings.py)

    Request/response cycle

        Client request > urls.py > backends.py > views.py > serializers.py > models.py...

        (when error raises > expecptions.py)

        ...models.py > serializers.py > renderers.py > Server response

    Update models in database

        (venv) ...apps> python manage.py makemigrations

        (update changes in models)

        (venv) ...apps> python manage.py makemigrations users

        (specify app name on first makemigrations of a new app)

        (venv) ...apps> python manage.py migrate

        (apply changes in database)

    Declare customizations in settings.py

        (enable custom model instead of default django.contrib.auth.models.User)

        AUTH_USER_MODEL = 'users.User'


        REST_FRAMEWORK = {

        (customize error handling)

        'EXCEPTION_HANDLER': 'apps.exceptions.core_exception_handler',

        'NON_FIELD_ERRORS_KEY': 'error',


        (define backend to authenticate requests or not)

        'DEFAULT_AUTHENTICATION_CLASSES': (

            'apps.users.backends.JWTAuthentication',

        )

        }

    Setup django-cors-headers

        (venv) ...apps> pip install django-cors-headers

        Modifications in settings.py:

        INSTALLED_APPS = [
            ...
            'corsheaders',
            ...
        ]

        MIDDLEWARE = [
            ...
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.common.CommonMiddleware',
            ...
        ]

        CorsMiddleware should be placed as high as possible, especially before any middleware that can generate responses such as Django's CommonMiddleware or Whitenoise's WhiteNoiseMiddleware. If it is not before, it will not be able to add the CORS headers to these responses.

        CORS_ORIGIN_ALLOW_ALL = True

    Create superuser

        (venv) ...apps> python manage.py createsuperuser

    Run python shell

        (venv) ...apps> python manage.py shell

        (venv) ...apps> python manage.py shell_plus

        (shell_plus automatically imports all models from apps in INSTALLED_APPS)

    Requests with curl
