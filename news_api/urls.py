from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter


schema_view = get_schema_view(
    openapi.Info(
        title="OpenSource News",
        default_version='v1',
        description=("Get Up To Date"),
        license=openapi.License(name="OpenSource News License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
]
