from django.urls import include, path
from . import views

urlpatterns = [
    path("robots.txt", views.robots_txt),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_builtin_user, name='login'),
    path('logout/', views.logout_builtin_user, name='logout'),
    path('upload/', views.upload_xls, name='upload'),
    path('classes/', views.list_classes, name='list.classes'),
    path('classes/add', views.edit_classe, name='add.classe'),
    path('classes/<classe_id>', views.show_classe, name='show.classe'),
    path('classes/<classe_id>/edit', views.edit_classe, name='edit.classe'),
    path('classes/<classe_id>/delete', views.delete_classe, name='delete.classe'),
    path('classes/<classe_id>/export', views.exportar_classe, name='exportar.xls'),
    path('classes/<classe_id>/exporting', views.wait_export, name='wait.export'),
    path('classes/<classe_id>/export/<export_name>', views.get_export, name='get.classe.export'),
    path('classes/<classe_id>/mailing', views.list_classe_mailings, name='list.classe.mailings'),
    path('classes/<classe_id>/mailing/new', views.editar_mailing_classe, name='nou.classe.mailing'),
    path('classes/<classe_id>/mailing/<mailing_id>', views.editar_mailing_classe, name='edit.classe.mailing'),
    path('classes/<classe_id>/mailing/<mailing_id>/send', views.enviar_mailing_classe, name='enviar.classe.mailing'),
    path('classes/<classe_id>/addalumne', views.edit_alumne, name='add.alumne'),
    path('classes/<classe_id>/<alumne_id>/edit', views.edit_alumne, name='edit.alumne'),
    path('classes/<classe_id>/<alumne_id>/delete', views.delete_alumne, name='delete.alumne'),
    path('alumnes/<alumne_id>', views.edit_alumne_form_pares, name='form.pares.edit.alumne'),
    path('mailing/cessiodades/<classe_id>', views.are_you_sure_email, name='send.cessio.dades.email'),
    path('mailing/<mailing_id>/attachment', views.afegir_attachment_mailing_classe, name='add.attachment.mailing'),
    path('mailing/<mailing_id>/attachment/<attachment_id>/remove', views.remove_attachment_mailing, name='remove.attachment.mailing'),
    path('help', views.show_help, name='show.help'),
    path('help/<topic>/index.html', views.show_help, name='show.topic'),
    path('help/<topic>/<file>.<ext>', views.redirect_to_static, name='redirct.static'),
    path('', views.home, name='home')
]