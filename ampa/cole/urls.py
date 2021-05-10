from django.urls import include, path
from . import views

urlpatterns = [
    path("robots.txt", views.robots_txt),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_builtin_user, name='login'),
    path('logout/', views.logout_builtin_user, name='logout'),
    
    # user management
    path('user/settings', views.user_settings, name='user.settings'),
    path('user/password/change', views.change_password, name='user.password.change'),
    
    # path('user/password/change/status', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # path('user/password/reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('user/password/reset/status', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('user/password/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('user/password/reset/status', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # staff settings
    path('staff/settings', views.staff_settings, name='staff.settings'),
    path('staff/entitat', views.edit_entitat, name='edit.entitat'),
    path('staff/entitat/logo', views.upload_entitat_logo, name='upload.logo.entitat'),
    path('staff/users', views.users_list, name='list.users'),
    path('staff/users/<user_slug>', views.edit_user, name='edit.user'),
    path('staff/users/<user_slug>/su', views.switch_user, name='switch.user'),

    # cursos
    path('cursos/', views.list_cursos, name='list.cursos'),
    path('cursos/modalitats', views.list_curs_modalitats, name='list.modalitats'),
    path('cursos/modalitats/add', views.edit_curs_modalitat, name='add.modalitat'),
    path('cursos/add', views.edit_curs, name='add.curs'),
    path('cursos/<curs_id>', views.show_curs, name='show.curs'),
    path('cursos/<curs_id>/edit', views.edit_curs, name='edit.curs'),
    path('cursos/<curs_id>/mailing', views.list_curs_mailings, name='list.curs.mailings'),
    path('cursos/<curs_id>/mailing/new', views.edit_mailing_curs, name='new.curs.mailing'),
    path('cursos/<curs_id>/mailing/<mailing_id>', views.edit_mailing_curs, name='edit.curs.mailing'),
    path('cursos/<curs_id>/mailing/<mailing_id>/show', views.show_mailing_curs, name='show.curs.mailing'),
    path('cursos/<curs_id>/mailing/<mailing_id>/send', views.enviar_mailing_curs, name='enviar.curs.mailing'),

    # etapes
    path('etapes/', views.list_etapes, name='list.etapes'),
    path('etapes/add', views.edit_etapa, name='add.etapa'),
    path('etapes/<etapa_id>', views.show_etapa, name='show.etapa'),
    path('etapes/<etapa_id>/edit', views.edit_etapa, name='edit.etapa'),
    path('etapes/<etapa_id>/mailing', views.list_etapa_mailings, name='list.etapa.mailings'),
    path('etapes/<etapa_id>/mailing/new', views.edit_mailing_etapa, name='new.etapa.mailing'),
    path('etapes/<etapa_id>/mailing/<mailing_id>', views.edit_mailing_etapa, name='edit.etapa.mailing'),
    path('etapes/<etapa_id>/mailing/<mailing_id>/show', views.show_mailing_etapa, name='show.etapa.mailing'),
    path('etapes/<etapa_id>/mailing/<mailing_id>/send', views.enviar_mailing_etapa, name='enviar.etapa.mailing'),

    # classes
    path('classes/', views.list_classes, name='list.classes'),
    path('classes/add', views.edit_classe, name='add.classe'),
    path('classes/<classe_id>', views.show_classe, name='show.classe'),
    path('classes/<classe_id>/edit', views.edit_classe, name='edit.classe'),
    path('classes/<classe_id>/delete', views.delete_classe, name='delete.classe'),
    path('classes/<classe_id>/upload/', views.upload_xls, name='upload.classe.xls'),
    path('classes/<classe_id>/upload/again/', views.reimport, name='upload.classe.xls.again'),
    path('classes/<classe_id>/export', views.exportar_classe, name='exportar.xls'),
    path('classes/<classe_id>/exporting', views.wait_export, name='wait.export'),
    path('classes/<classe_id>/export/<export_name>', views.get_export, name='get.classe.export'),
    path('classes/<classe_id>/mailing', views.list_classe_mailings, name='list.classe.mailings'),
    path('classes/<classe_id>/mailing/new', views.editar_mailing_classe, name='nou.classe.mailing'),
    path('classes/<classe_id>/mailing/<mailing_id>', views.editar_mailing_classe, name='edit.classe.mailing'),
    path('classes/<classe_id>/mailing/<mailing_id>/show', views.show_mailing_classe, name='show.classe.mailing'),
    path('classes/<classe_id>/mailing/<mailing_id>/send', views.enviar_mailing_classe, name='enviar.classe.mailing'),
    path('classes/<classe_id>/addalumne', views.edit_alumne, name='add.alumne'),
    path('classes/<classe_id>/alumne/<alumne_id>/add', views.add_alumne_classe, name='add.alumne.classe'),
    path('classes/<classe_id>/addalumne/search', views.add_classe_search_alumne, name='add.classe.search.alumne'),
    path('classes/<classe_id>/<alumne_id>/edit', views.edit_alumne, name='edit.alumne'),
    path('classes/<classe_id>/<alumne_id>/delete', views.delete_alumne, name='delete.alumne'),

    # alumnes
    path('alumnes/<alumne_id>', views.edit_alumne_form_pares, name='form.pares.edit.alumne'),
    path('alumnes/<alumne_id>/classes', views.edit_alumne_classes, name='list.alumne.classes'),
    path('alumnes/<alumne_id>/classes/<classe_id>/unlink', views.unlink_alumne_classes, name='unlink.alumne.classes'),
    path('alumnes/<alumne_id>/edit', views.search_edit_alumne, name='search.edit.alumne'),
    path('alumnes/<alumne_id>/extra/add', views.edit_extrainfo_alumne, name='add.extrainfo.alumne'),
    path('alumnes/<alumne_id>/extra/<extrainfo_id>/edit', views.edit_extrainfo_alumne, name='edit.extrainfo.alumne'),

    # general mailing
    path('mailing/cessiodades/<classe_id>', views.are_you_sure_email, name='send.cessio.dades.email'),
    path('mailing/<mailing_id>/attachment', views.afegir_attachment_mailing_classe, name='add.attachment.mailing'),
    path('mailing/<mailing_id>/attachment/<attachment_id>/remove', views.remove_attachment_mailing, name='remove.attachment.mailing'),

    # templates
    path('plantilles/', views.list_templates, name='peticions.list.templates'),
    path('plantilles/upload', views.upload_template, name='peticions.add.template'),

    # ajuda inline
    path('help', views.show_help, name='show.help'),
    path('help/<topic>/index.html', views.show_help, name='show.topic'),
    path('help/<topic>/<file>.<ext>', views.help_media_redirect_to_static, name='help.media.redirect.static'),
    path('sr/<path:file>', views.redirect_to_static, name='redirect.static'),
    path('', views.home, name='home')
]