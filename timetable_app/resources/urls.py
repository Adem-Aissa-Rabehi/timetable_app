from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
  # Salles
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('rooms/edit/<int:room_id>/', views.edit_room, name='edit_room'),  # URL pour modifier une salle

    # Domaines
    path('domains/', views.domain_list, name='domain_list'),
    path('domains/add/', views.add_domain, name='add_domain'),
    path('domains/edit/<int:domain_id>/', views.edit_domain, name='edit_domain'),  # URL pour modifier un domaine

    # Formations
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/add/', views.add_formation, name='add_formation'),
    path('formations/edit/<int:formation_id>/', views.edit_formation, name='edit_formation'),  # URL pour modifier une formation

    # Modules
    path('modules/', views.module_list, name='module_list'),
    path('modules/add/', views.add_module, name='add_module'),
    path('modules/edit/<int:module_id>/', views.edit_module, name='edit_module'),  # URL pour modifier un module

    # Professeurs
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('teachers/edit/<int:teacher_id>/', views.edit_teacher, name='edit_teacher'),  # URL pour modifier un professeur

    # Groupes
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.add_group, name='add_group'),
    path('groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),  # URL pour modifier un groupe

    # Cours
    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),  # URL pour modifier un cours

    # Calendrier
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/data/', views.calendar_data, name='calendar_data'),  # Données pour FullCalendar

    # Exportation
    path('export-courses-csv/', views.export_courses_csv, name='export_courses_csv'),
    path('export-courses-pdf/', views.export_courses_pdf, name='export_courses_pdf'),

    # Planification Automatique
    path('auto-schedule-course/<int:course_id>/', views.auto_schedule_course, name='auto_schedule_course'),
    path('auto-schedule-all-courses/', views.auto_schedule_all_courses, name='auto_schedule_all_courses'),

    # Sessions Manuelles
    path('save-manual-session/', views.save_manual_session, name='save_manual_session'),

    path('rooms/delete/<int:room_id>/', views.delete_room, name='delete_room'),
path('domains/delete/<int:domain_id>/', views.delete_domain, name='delete_domain'),
path('formations/delete/<int:formation_id>/', views.delete_formation, name='delete_formation'),
path('modules/delete/<int:module_id>/', views.delete_module, name='delete_module'),
path('teachers/delete/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'), 
path('groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
]