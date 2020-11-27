from django.urls import include, path
from . import views

urlpatterns = [
    path('liveness', views.liveness, name='health.liveness'),
    path('readiness', views.liveness, name='health.readiness'),
]