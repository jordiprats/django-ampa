from django.urls import include, path
from . import views

urlpatterns = [
    # juntes
    path('', views.list_juntes, name='peticions.list.juntes'),
    path('/add', views.edit_junta, name='peticions.add.junta'),
    # categories
    path('peticions/categories', views.list_categories, name='peticions.list.categories'),
    path('peticions/categories/add', views.edit_category, name='peticions.add.category'),
    path('peticions/categories/edit/<category_id>', views.edit_category, name='peticions.edit.category'),
    # issues
    path('peticions', views.list_issues, name='peticions.list.issues'),
    path('peticions/add', views.edit_issue, name='peticions.add.issue'),
    path('peticions/<issue_id>/edit', views.edit_issue, name='peticions.edit.issue'),
    path('peticions/<issue_id>/show', views.show_issue, name='peticions.show.issue'),
    # comments
    path('peticions/<issue_id>/comments/add', views.edit_comment, name='peticions.add.comment'),
]
