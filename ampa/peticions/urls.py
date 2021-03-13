from django.urls import include, path
from . import views

urlpatterns = [
    # juntes
    path('', views.list_juntes, name='peticions.list.juntes'),
    path('add', views.edit_junta, name='peticions.add.junta'),
    path('<junta_id>/edit', views.edit_junta, name='peticions.edit.junta'),
    path('<junta_id>/show', views.show_junta, name='peticions.show.junta'),
    path('<junta_id>/pdf/preview', views.preview_pdf, name='peticions.preview_pdf.junta'),
    path('<junta_id>/delete', views.delete_junta, name='peticions.delete.junta'),
    path('<junta_id>/publish', views.publish_junta, name='peticions.publish.junta'),
    path('<junta_id>/edit/peticions', views.list_junta_peticio, name='peticions.edit.junta.list.peticions'),
    path('<junta_id>/edit/peticions/add/all', views.add_all_junta_peticio, name='peticions.junta.add.all.peticions'),
    path('<junta_id>/edit/peticions/<issue_id>/add', views.add_junta_peticio, name='peticions.edit.junta.add.peticio'),
    path('<junta_id>/edit/peticions/<issue_id>/remove', views.remove_junta_peticio, name='peticions.edit.junta.remove.peticio'),
    path('actes/<junta_slug>', views.show_acte_junta, name='peticions.show.acte.junta'),
    # categories
    path('peticions/categories', views.list_categories, name='peticions.list.categories'),
    path('peticions/categories/add', views.edit_category, name='peticions.add.category'),
    path('peticions/categories/<category_id>/edit', views.edit_category, name='peticions.edit.category'),
    path('peticions/categories/<category_id>/delete', views.delete_category, name='peticions.delete.category'),
    # representants
    path('peticions/representants', views.list_representants, name='peticions.list.representants'),
    path('peticions/representants/add', views.edit_representant, name='peticions.add.representant'),
    path('peticions/representants/<representant_id>/edit', views.edit_representant, name='peticions.edit.representant'),
    path('peticions/representants/<representant_id>/delete', views.delete_representant, name='peticions.delete.representant'),
    # issues
    path('peticions', views.list_issues, name='peticions.list.issues'),
    path('peticions/add', views.edit_issue, name='peticions.add.issue'),
    path('peticions/forward/open', views.forward_open_peticions, name='peticions.forward.open'),
    path('peticions/<issue_id>/edit', views.edit_issue, name='peticions.edit.issue'),
    path('peticions/<issue_id>/show', views.show_issue, name='peticions.show.issue'),
    path('peticions/<issue_id>/like', views.like_issue, name='peticions.like.issue'),
    path('peticions/<issue_id>/dislike', views.dislike_issue, name='peticions.dislike.issue'),
    path('peticions/<issue_id>/delete', views.delete_issue, name='peticions.delete.issue'),
    # comments
    path('peticions/<issue_id>/comments/add', views.edit_comment, name='peticions.add.comment'),
    path('peticions/<issue_id>/comments/<comment_id>/edit', views.edit_comment, name='peticions.edit.comment'),
    path('peticions/<issue_id>/comments/<comment_id>/delete', views.delete_comment, name='peticions.delete.comment'),
]
