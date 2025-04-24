import os
from pathlib import Path
import pymysql


pymysql.install_as_MySQLdb()



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yg@h3)ix@0-uk7c(y$lupklzv#umsk5#*t3q*1^j+r#()iv&=h'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'carRental',
    'PaymentApp',
    'paypal.standard.ipn',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'Car_rental.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # ✅ Needed for request.user
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'Car_rental.wsgi.application'

# Database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#         'OPTIONS': {
#             'timeout': 20,  # Timeout in seconds (adjust as needed)
#         },
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ride_on_rent',         # Replace with your DB name
        'USER': 'root',      # Replace with your MySQL username
        'PASSWORD': 'root',    # Replace with your MySQL password
        'HOST': 'localhost',            # Or your remote DB host
        'PORT': '3306',                 # Default MySQL port
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
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

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# PayPal settings
# PAYPAL_RECEIVER_EMAIL = 'sb-3ax3q31674302@business.example.com'  # your PayPal account email
# PAYPAL_TEST = True  # Enable sandbox mode for testing
# PAYPAL_CLIENT_ID = 'AaaeaF-QZD4LYt3DnX78W-_RfuoP02L92d0iKw-mdTbMBAoVqmuIaxkhsfhi_v6TM49tBR6GOQkyc8QA'
# PAYPAL_CLIENT_SECRET = 'EEzNTgopyPN-DHilEzGO3iLdhPhZac90j7DzVX1aANeeWvVr5AAJMesWpnSMMcaj54fEa5SSDCFqQOXk'
# PAYPAL_API_BASE = 'https://api-m.sandbox.paypal.com'

PAYPAL_RECEIVER_EMAIL = 'sb-3ax3q31674302@business.example.com' # where cash is paid into
PAYPAL_TEST = True
PAYPAL_CLIENT_ID = 'AaaeaF-QZD4LYt3DnX78W-_RfuoP02L92d0iKw-mdTbMBAoVqmuIaxkhsfhi_v6TM49tBR6GOQkyc8QA'
PAYPAL_CLIENT_SECRET = 'EEzNTgopyPN-DHilEzGO3iLdhPhZac90j7DzVX1aANeeWvVr5AAJMesWpnSMMcaj54fEa5SSDCFqQOXk'
PAYPAL_API_BASE = 'https://api-m.sandbox.paypal.com'

# URLs for PayPal return and cancel actions
PAYPAL_RETURN_URL = 'http://127.0.0.1:8000/payment_done/'
PAYPAL_CANCEL_URL = 'http://127.0.0.1:8000/payment_cancelled/'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'rideonrentt2407@gmail.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'gmls bssg enhp kqsn')
EMAIL_USE_SSL = False

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ADMIN_EMAIL = 'rideonrentt2407@gmail.com'