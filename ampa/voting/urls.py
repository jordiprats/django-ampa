from django.urls import include, path
from . import views

urlpatterns = [
    path('poll/add', views.edit_election, name='voting.add.election'),
    path('poll/list', views.list_elections, name='voting.list.elections'),
    path('poll/<election_id>/edit', views.edit_election, name='voting.edit.election'),
    path('poll/<election_id>/option/add', views.edit_option, name='voting.add.option'),
    path('poll/<election_id>/option/<option_id>/edit', views.edit_option, name='voting.edit.option'),
    path('poll/<election_id>/option/<option_id>/delete', views.delete_option, name='voting.delete.option'),
    #path('election/<election_id>/<election_token>', views.show_election, name='voting.show.election'),
    path('', views.home, name='voting.home')
]