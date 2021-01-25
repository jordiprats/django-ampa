from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.list_issues, name='peticions.list.issues'),
]
