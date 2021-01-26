from django.urls import include, path
from . import views

urlpatterns = [
    path('categories', views.list_categories, name='peticions.list.categories'),
    path('categories/add', views.edit_category, name='peticions.add.category'),
    path('categories/edit/<category_id>', views.edit_category, name='peticions.edit.category'),
    # issues
    path('', views.list_issues, name='peticions.list.issues'),
    path('add', views.edit_issue, name='peticions.add.issue'),
    path('<issue_id>/edit', views.edit_issue, name='peticions.edit.issue'),
    path('<issue_id>/show', views.show_issue, name='peticions.show.issue'),
    # comments
    path('<issue_id>/comments/add', views.edit_comment, name='peticions.add.comment'),
]
