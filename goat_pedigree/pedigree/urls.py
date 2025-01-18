# pedigree/urls.py
from django.conf.urls import handler404
from django.urls import path
from . import views

urlpatterns = [
    path('goat-profiles/', views.goat_profiles, name='goat_profiles'),
    path('pedigree-charts/', views.pedigree_charts, name='pedigree_charts'),
    path('reports/', views.reports, name='reports'),
    path('about/', views.about, name='about'),
]

# Set the custom 404 handler
handler404 = views.custom_404
