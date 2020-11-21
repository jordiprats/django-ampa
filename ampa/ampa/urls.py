from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('site-admin/', admin.site.urls),
    path('', include('cole.urls')),
    path('votacions/', include('voting.urls'))
]
