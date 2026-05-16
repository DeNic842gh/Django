from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
try:
    from rest_framework_simplejwt.views import (
        TokenObtainPairView,
        TokenRefreshView,
    )
    jwt_views_available = True
except Exception:
    TokenObtainPairView = None
    TokenRefreshView = None
    jwt_views_available = False
from django.urls import re_path
from rest_framework import permissions

# drf_yasg (Swagger) optional import — guard for environments without pkg_resources
try:
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Pirate Restaurant API",
            default_version='v1',
            description='OpenAPI schema for Pirate Restaurant',
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
except Exception:
    schema_view = None

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

if jwt_views_available:
    urlpatterns += [
        path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ]

# Conditionally expose Swagger endpoints only when drf_yasg is available
if schema_view:
    urlpatterns += [
        re_path(r'^swagger(?P<format>\\.json|\\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
