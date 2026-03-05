from pathlib import Path
from datetime import timedelta  # ← Agregar al inicio del archivo
from django.urls import path, include

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pu2jb$jlm8(m6z0ep02w)9rdx)dw&7ajn)a_kd+73h2h_=3#cm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if not DEBUG:
    # Forzar HTTPS
    SECURE_SSL_REDIRECT = True
    
    # Cookies seguras
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # Headers de seguridad
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    
    # HSTS (HTTP Strict Transport Security)
    SECURE_HSTS_SECONDS = 31536000  # 1 año
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Proxy SSL headers
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'daphne',  # ← DEBE SER LA PRIMERA
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Apps de terceros
    'rest_framework',
    'corsheaders',
    'channels',         # ← AGREGAR
    'graphene_django',    # ← AGREGAR
    'oauth2_provider',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'libros',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'libros.middleware.SecurityMiddleware',
    'libros.middleware.RateLimitMiddleware',  # ← AGREGAR
]

ROOT_URLCONF = 'biblioteca_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # ← AGREGAR esto
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

# Busca la línea de WSGI y agrega la de ASGI justo debajo
WSGI_APPLICATION = 'biblioteca_project.wsgi.application'
ASGI_APPLICATION = 'biblioteca_project.asgi.application' # ← AGREGA ESTA LÍNEA


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'biblioteca_uni4',
        'USER': 'root',
        'PASSWORD': '', 
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8', 
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', default_storage_engine=INNODB",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# ==============================
# CONFIGURACIÓN DE CORS
# ==============================
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://tudominio.com",
    "https://www.tudominio.com",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    "https://tudominio.com",
    "https://www.tudominio.com",
]

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Strict'

# =======================
# REST FRAMEWORK CONFIG
# =======================

REST_FRAMEWORK = {
    # AUTENTICACIÓN: Qué métodos acepta tu API
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT (Token moderno)
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',  # ← AGREGAR para OAuth 2.0
        'rest_framework.authentication.TokenAuthentication',          # Token tradicional
        'rest_framework.authentication.SessionAuthentication',        # Sesión (para admin)
    ],
    
    # PERMISOS: Qué pueden hacer los usuarios
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    
    # PAGINACIÓN: Cuántos resultados por página
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    
    # FILTROS: Permitir búsquedas y ordenamiento
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],

        'DEFAULT_THROTTLE_CLASSES': [
        'libros.throttles.BurstRateThrottle',
        'libros.throttles.SustainedRateThrottle',
    ],
    
    'DEFAULT_THROTTLE_RATES': {
        'burst': '60/min',        # 60 por minuto
        'sustained': '1000/day',  # 1000 por día
        'anon_burst': '20/min',   # Anónimos: 20 por minuto
        'premium': '10000/day',   # Premium: 10000 por día
    }
}

# =======================
# SIMPLE JWT CONFIG
# =======================

SIMPLE_JWT = {
    # ⏱️ DURACIÓN DE TOKENS
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),    # Token de acceso válido 1 hora
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),    # Token de refresco válido 7 días
    
    # 🔄 ROTACIÓN DE TOKENS (Seguridad extra)
    'ROTATE_REFRESH_TOKENS': True,                  # Genera nuevo refresh al refrescar
    'BLACKLIST_AFTER_ROTATION': True,               # Invalida el refresh anterior
    'UPDATE_LAST_LOGIN': True,                      # Actualiza last_login del usuario
    
    # 🔐 ALGORITMO Y CLAVE DE FIRMA
    'ALGORITHM': 'HS256',                           # HMAC SHA-256 (más común)
    'SIGNING_KEY': SECRET_KEY,                      # Usa la SECRET_KEY de Django
    'VERIFYING_KEY': None,                          # Solo para algoritmos asimétricos (RSA)
    
    # 📋 CONFIGURACIÓN DE HEADERS
    'AUTH_HEADER_TYPES': ('Bearer',),               # Tipo: "Authorization: Bearer TOKEN"
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',       # Nombre del header
    
    # 👤 CLAIMS DEL USUARIO
    'USER_ID_FIELD': 'id',                          # Campo del modelo User para ID
    'USER_ID_CLAIM': 'user_id',                     # Nombre del claim en el payload
    
    # 🎫 CONFIGURACIÓN DEL TOKEN
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',               # Claim que identifica tipo de token
    'JTI_CLAIM': 'jti',                             # JWT ID (identificador único)
}

# ==============================
# CONFIGURACIÓN DE IDIOMA Y ZONA HORARIA
# ==============================
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Hermosillo'  # Hermosillo
USE_I18N = True
USE_TZ = True

# =======================
# SITE CONFIGURATION
# =======================
SITE_ID = 1  # ← AGREGAR

# =======================
# AUTHENTICATION BACKENDS
# =======================
AUTHENTICATION_BACKENDS = [
    # Backend por defecto de Django (username/password)
    'django.contrib.auth.backends.ModelBackend',
    
    # Backend de allauth para OAuth social
    'allauth.account.auth_backends.AuthenticationBackend',
]

# =======================
# DJANGO ALLAUTH CONFIG
# =======================

# Configuración de cuentas
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False  # Solo email para login social
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'optional'  # Para desarrollo: 'mandatory' en producción

# Configuración de login social
SOCIALACCOUNT_AUTO_SIGNUP = True  # Crear usuario automáticamente
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # No verificar email en OAuth

# Proveedores OAuth configurados
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '245061395600-jlptmi6srcjdutjajkp7h7gbr8hqapgg.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# =======================
# OAUTH 2.0 PROVIDER SETTINGS
# =======================
# Configuración para django-oauth-toolkit
OAUTH2_PROVIDER = {
    'SCOPES': {
        'read': 'Read scope - Permite leer datos',
        'write': 'Write scope - Permite escribir datos',
        'groups': 'Access to groups - Acceso a grupos de usuario'
    },
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 hora
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400,  # 1 día
    'AUTHORIZATION_CODE_EXPIRE_SECONDS': 600,  # 10 minutos
    'ROTATE_REFRESH_TOKEN': True,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SILENCED_SYSTEM_CHECKS = ['models.W036']

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}