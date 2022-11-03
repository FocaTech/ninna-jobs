from django.contrib import admin
from django.urls import path, include, re_path as url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import RedirectView
from django.template.response import TemplateResponse

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), #debug false
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), #debug fale
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')), #debug false
    path('admin/', admin.site.urls),
    path('conta/', include("login_cadastro.urls")),
    path('vaga/', include("vaga.urls")),
    path('', include("vaga.urls")),
    path('usuarios/', include("usuarios.urls")),
    path('ninna/', include("admin.urls")),
    url(r'^', TemplateResponse, {'template': '404.html'}),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)