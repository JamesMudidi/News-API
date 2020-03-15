from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/v1/', include('authentication.urls')),
]
