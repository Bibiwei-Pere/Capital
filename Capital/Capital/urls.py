from django.contrib import admin
from django.urls import path, include 
from main.views import *
from main.admin import *
from django.contrib.staticfiles.urls import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', WelcomeView.as_view(), name='home'),
    path('',include('main.urls')),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    
    path('activate/(P<uidb64>[0-9A-Za-z_\-]+)/(P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',activate, name='activate'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)