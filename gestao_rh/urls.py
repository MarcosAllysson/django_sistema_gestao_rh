"""gestao_rh URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static

# Internacionalização
from django.conf.urls.i18n import i18n_patterns

# Django rest framework
from rest_framework import routers
from core import views

# APIs
from funcionarios.api.viewsets import FuncionarioViewSet
from registro_hora_extra.api.viewsets import RegistroHoraExtraViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'api/funcionarios', FuncionarioViewSet)
router.register(r'api/horas-extras', RegistroHoraExtraViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += i18n_patterns (
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('funcionarios/', include('funcionarios.urls')),
    path('documentos/', include('documentos.urls')),
    path('horas-extras/', include('registro_hora_extra.urls')),
    path('empresas/', include('empresas.urls')),
    path('departamentos/', include('departamentos.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # Django rest framework
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
