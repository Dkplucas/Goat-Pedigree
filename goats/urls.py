from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views
from goats.views import CustomLogoutView
from django.conf import settings
from django.conf.urls.static import static


# Initialize the DefaultRouter
router = DefaultRouter()
router.register(r'goats', views.GoatViewSet, basename='goat')

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    path('api/goats/', views.get_goat_data, name='goat-data'),  # Custom API endpoint
    
    # Frontend views
    path('', views.home, name='home'),  # Home page
    path('inventory/', views.inventory, name='inventory'),  # Inventory page
    path('tree/', views.tree, name='tree'),  # Tree page
    path('reports/', views.reports, name='reports'),  # Reports page
    path("about/", views.about, name="about"),  # About page path('registration/login/', views.signup),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    
   
]

# Development-only URLs (media files)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # If DEBUG=False, manually serve media files (NOT RECOMMENDED FOR PRODUCTION)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
