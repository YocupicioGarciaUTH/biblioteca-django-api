# biblioteca_project/urls.py

from django.contrib import admin
from django.urls import path, include
from .jwt_views import CustomTokenObtainPairView
from libros import web_views 
from django.shortcuts import render, redirect
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# 1. IMPORTA TU ESQUEMA DE GRAPHQL AQUÍ
from libros.schema import schema 

urlpatterns = [
    # Admin de Django
    path('admin/', admin.site.urls),
    
    # URLs de la API
    path('api/', include('libros.api_urls')),

    # OAuth URLs de allauth
    path('accounts/', include('allauth.urls')),
    
    # OAuth 2.0 URLs de django-oauth-toolkit
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    # JWT personalizado
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),

    # Vistas Web
    path('', web_views.home, name='home'),
    path('oauth/login/', web_views.oauth_login, name='oauth_login'),
    path('login/jwt/', web_views.jwt_login_page, name='jwt_login_page'),
    
    # 2. RUTA CORREGIDA: Se añade 'schema=schema' para evitar el AssertionError
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]