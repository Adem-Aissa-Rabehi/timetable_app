from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('domains/', views.domain_list, name='domain_list'),
    path('domains/add/', views.add_domain, name='add_domain'),
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/add/', views.add_formation, name='add_formation'),
    path('modules/', views.module_list, name='module_list'),
    path('modules/add/', views.add_module, name='add_module'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.add_teacher, name='add_teacher'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.add_group, name='add_group'),
    path('', views.course_list, name='course_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/export/csv/', views.export_courses_csv, name='export_courses_csv'),
    path('courses/export/pdf/', views.export_courses_pdf, name='export_courses_pdf'),
    path('courses/calendar/', views.course_calendar, name='course_calendar'),
]