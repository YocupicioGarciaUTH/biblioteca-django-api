from django.contrib import admin
from django.urls import path, include
from libros import web_views  # ← AGREGAR
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # URLs de la API
    path('api/', include('libros.api_urls')),
    
    # URLs de páginas web (para pruebas)
    path('', web_views.home, name='home'),
    path('oauth/login/', TemplateView.as_view(template_name='oauth_login.html'), name='oauth_login'),
    path('login/jwt/', web_views.jwt_login_page, name='jwt_login_page'),
]