import os
from pathlib import Path
from dotenv import load_dotenv
from utils.environement import convert_str_to_list

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DEBUG: bool = True if os.environ.get('DEBUG') == '0' else False

ALLOWED_HOSTS: list[str] = convert_str_to_list('ALLOWED_HOSTS')

ROOT_URLCONF = 'project.urls'

WSGI_APPLICATION = 'project.wsgi.application'


CSRF_TRUSTED_ORIGINS: list[str] = convert_str_to_list('CSRF_TRUSTED_ORIGINS')
