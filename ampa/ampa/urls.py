from django.contrib import admin
from django.urls import path, include

import os

urlpatterns = [
    path('prometheus/', include('django_prometheus.urls')),
    path('health/', include('health.urls')),
    path('', include('cole.urls')),
    path('votacions/', include('voting.urls')),
    path('juntes/', include('peticions.urls'))
]

if os.getenv('DEBUG', False):
    urlpatterns.append(path('site-admin/', admin.site.urls))