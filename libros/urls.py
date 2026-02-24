from ..biblioteca_project.jwt_views import CustomTokenObtainPairView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # JWT personalizado
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),
    # ... resto
]