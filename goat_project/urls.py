"""
URL configuration for goat_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# goat_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from goats import views
from django.conf.urls import handler404
from goats.views import CustomLoginView
from goats.views import CustomLogoutView
from goats import views as goats_views
from django.views.generic import TemplateView
from django.conf.urls import handler404
from goats.views import custom_404_view

# Django admin header customization
admin.site.site_header = "Goat Pedigree Admin"
admin.site.site_title = "Goat Pedigree Admin Portal"
admin.site.index_title = "Welcome to Goat Pedigree Admin Portal"

# URL patterns
urlpatterns = [
    path('admin/login/', CustomLoginView.as_view()),  # Override the admin login URL
    path('admin/logout/', CustomLogoutView.as_view()),  # Override the admin logout URL
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', include('goats.urls')),  # Include your app's URLs
    path('__reload__/', include('django_browser_reload.urls')),  # Add this line
    path('404-test/', TemplateView.as_view(template_name='404.html')),
    
]

# Set the custom 404 handler
handler404 = 'goats.views.custom_404_view'

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # If DEBUG=False, manually serve media files (NOT RECOMMENDED FOR PRODUCTION)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




