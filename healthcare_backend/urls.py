"""
URL configuration for healthcare_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Authentication APIs
    path('api/auth/', include('authentication.urls')),

    # 2. Patient Management APIs
    path('api/patients/', include('patients.urls')),

    # 3. Doctor Management APIs
    path('api/doctors/', include('doctors.urls')),

    # 4. Patient-Doctor Mapping APIs
    path('api/mappings/', include('mappings.urls')),

    # API Documentation (Swagger & Redoc)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
