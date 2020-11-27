from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('prometheus/', include('django_prometheus.urls')),
    path('health/', include('health.urls')),
    path('site-admin/', admin.site.urls),
    path('', include('cole.urls')),
    path('votacions/', include('voting.urls'))
]
