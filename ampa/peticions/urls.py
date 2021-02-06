from django.urls import include, path
from . import views

urlpatterns = [
    # juntes
    path('', views.list_juntes, name='peticions.list.juntes'),
    path('add', views.edit_junta, name='peticions.add.junta'),
    path('<junta_id>/edit', views.edit_junta, name='peticions.edit.junta'),
    path('<junta_id>/edit/peticions', views.list_junta_peticio, name='peticions.edit.junta.list.peticions'),
    path('<junta_id>/edit/peticions/<issue_id>/add', views.add_junta_peticio, name='peticions.edit.junta.add.peticio'),
    path('<junta_id>/edit/peticions/<issue_id>/remove', views.remove_junta_peticio, name='peticions.edit.junta.remove.peticio'),
    # categories
    path('peticions/categories', views.list_categories, name='peticions.list.categories'),
    path('peticions/categories/add', views.edit_category, name='peticions.add.category'),
    path('peticions/categories/edit/<category_id>', views.edit_category, name='peticions.edit.category'),
    # issues
    path('peticions', views.list_issues, name='peticions.list.issues'),
    path('peticions/add', views.edit_issue, name='peticions.add.issue'),
    path('peticions/<issue_id>/edit', views.edit_issue, name='peticions.edit.issue'),
    path('peticions/<issue_id>/show', views.show_issue, name='peticions.show.issue'),
    path('peticions/<issue_id>/like', views.like_issue, name='peticions.like.issue'),
    path('peticions/<issue_id>/dislike', views.dislike_issue, name='peticions.dislike.issue'),
    path('peticions/<issue_id>/delete', views.delete_issue, name='peticions.delete.issue'),
    # comments
    path('peticions/<issue_id>/comments/add', views.edit_comment, name='peticions.add.comment'),
]
