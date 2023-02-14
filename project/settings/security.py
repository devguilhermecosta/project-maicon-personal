# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-13esnkz+4nxkgs6%@efr^r)v)woeh@@*#l3+@vvjgx4#b3vp7y'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
