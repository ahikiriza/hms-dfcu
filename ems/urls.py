"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Configure schema view
schema_view = get_schema_view(
    openapi.Info(
        title="DFCU Bank HR Management System API",
        default_version='v1',
        description="This API enables staff registration, retrieval, and updates for the dfcu Bank HR Management System, supporting onboarding and management of employees.",
        terms_of_service="https://www.dfcubank.com/terms",
        contact=openapi.Contact(email="support@dfcubank.com"),
        license=openapi.License(name="BSD License"),
    ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls,name="admin-site"),
    path('staff_app/', include('employee_information.api_urls')),
    path('', include('employee_information.urls')),
    # path('staff_app/', include('staff_app.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
