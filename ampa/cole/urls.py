from django.urls import include, path
from . import views

urlpatterns = [
    path("robots.txt", views.robots_txt),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_builtin_user, name='login'),
    path('logout/', views.logout_builtin_user, name='logout'),
    path('upload/', views.upload_xls, name='upload'),
    path('classes/', views.list_classes, name='list.classes'),
    path('classes/<classe_id>', views.show_classe, name='show.classe'),
    path('alumnes/<alumne_id>', views.edit_alumne, name='edit.alumne'),
    path('email/<classe_id>', views.are_you_sure_email, name='send.email'),
    path('', views.home, name='home')
]