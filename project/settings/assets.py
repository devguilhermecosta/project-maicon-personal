from . environment import BASE_DIR


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / 'base_static',
]

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGE_CODE = 'en-us'
