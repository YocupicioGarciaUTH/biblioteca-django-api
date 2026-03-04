from pathlib import Path
from datetime import timedelta  # ← Agregar al inicio del archivo

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pu2jb$jlm8(m6z0ep02w)9rdx)dw&7ajn)a_kd+73h2h_=3#cm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # ← AGREGAR (requerido por allauth)
    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework_simplejwt',
    'oauth2_provider',  # ← AGREGAR (Django OAuth Toolkit)
    'allauth',  # ← AGREGAR
    'allauth.account',  # ← AGREGAR
    'allauth.socialaccount',  # ← AGREGAR
    'allauth.socialaccount.providers.google',  # ← AGREGAR
    'django_extensions',

    # Tu aplicación
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
    'allauth.account.middleware.AccountMiddleware',  # ← AGREGAR
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

WSGI_APPLICATION = 'biblioteca_project.wsgi.application'


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
]
CORS_ALLOW_CREDENTIALS = True


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
    # Tiempo de vida de los tokens
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,  # 1 hora
    'REFRESH_TOKEN_EXPIRE_SECONDS': 86400 * 7,  # 7 días
    
    # Scopes disponibles
    'SCOPES': {
        'read': 'Acceso de lectura',
        'write': 'Acceso de escritura',
    },
    
    # Tipo de token por defecto
    'ACCESS_TOKEN_MODEL': 'oauth2_provider.AccessToken',
    'REFRESH_TOKEN_MODEL': 'oauth2_provider.RefreshToken',
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SILENCED_SYSTEM_CHECKS = ['models.W036']