from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conta/', include("login_cadastro.urls")),
    path('vaga/', include("vaga.urls")),
    path('', include("vaga.urls")),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)