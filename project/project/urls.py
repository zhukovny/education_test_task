from django.contrib import admin
from django.template.defaulttags import url
from django.urls import include
from django.urls import path
from django.urls import re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="Organization API",
        default_version='v1',
        description="Some description",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    patterns=[path('organization/', include('organization.urls'))],
    public=True,
)


urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path('organization/', include('organization.urls')),
]
