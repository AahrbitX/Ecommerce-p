 
import os
from pathlib import Path
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = 'django-insecure-hvo8u$w_p)z*gsd(%&lo9trxo=s^*vkp+u)&ctf)$6!#rq@(th'
 
DEBUG = True

ALLOWED_HOSTS = ['*']

 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    #apps
    'products',
    'common',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS = ['*']

CORS_ALLOW_METHODS = ["*"]

CORS_ALLOW_CREDENTIALS = True 

CORS_ALLOWED_ORIGINS = [
    'http://*',
    'https://*',
]
CSRF_TRUSTED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "x-requested-with",
    "Accept",
    "Origin",
    # Add other headers if necessary
]

ROOT_URLCONF = 'root.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'root.wsgi.application'

 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

APPEND_SLASH = False


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
 

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

 
 

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = 'static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

#images
MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/') 


AUTH_USER_MODEL = 'common.CustomUser'
 

AUTHENTICATION_BACKENDS = [
    'common.backends.EmailBackend',       
    'django.contrib.auth.backends.ModelBackend',   ]
 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
       
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        #   'common.backends.CookieJWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),   
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),      
    'ROTATE_REFRESH_TOKENS': True,
    # 'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'user_id',
    'USER_ID_CLAIM': 'user_id',
     
}

EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))   
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() in ["true", "1", "yes"]  
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "maneeshmaneesh391@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "ufmd xzkl sgol nuxu")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "maneeshmaneesh391@gmail.com")



# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',  # Only logs when DEBUG is False
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',  # Change to WARNING or ERROR to reduce verbosity
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'required.log'),  # Log file location
            'formatter': 'verbose',
        },
        'error_file': {  # Separate file for critical errors
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'errors.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file'],  # Log general info and errors separately
            'level': 'INFO',  # Set to WARNING or ERROR if needed
            'propagate': True,
        },
        'custom_logger': {   
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
