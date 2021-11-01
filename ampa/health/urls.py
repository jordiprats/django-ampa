from django.urls import include, path
from . import views

urlpatterns = [
    path('liveness', views.liveness, name='health.liveness'),
    path('readiness', views.readiness, name='health.readiness'),
    path('startup', views.startup, name='health.startup'),
]