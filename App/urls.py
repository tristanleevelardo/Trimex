from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('student/<str:student_name>/', views.student, name='student'),


    path('faculty/',views.faculty, name='faculty' ),
    path('facultyPage/<str:faculty_name>/',views.facultyPage, name='facultyPage' ),
    path('unit/<str:faculty_name>/<str:subject>/<str:course>/', views.facultyUnit, name='unit'),
    path('edit_student/<str:student_name>/<str:student_subject>/', views.edit_student, name='edit_student'),
    
    
    path('mail_student/<str:student_name>/', views.mail_student, name='mail_student'),
    path('student_profile/<str:student_name>/', views.student_profile, name='student_profile'),
    path('mail_message/<str:student_name>/<str:instructor_name>/', views.mail_message, name='mail_message'),

    path('faculty_profile/<str:instructor_name>/', views.faculty_profile, name='faculty_profile'),
    path('mail_faculty/<str:instructor_name>/', views.mail_faculty, name='mail_faculty'),
    path('mail_message_faculty/<str:student_name>/<str:instructor_name>/', views.mail_message_faculty, name='mail_message_faculty'),

    path('delete_mail/<int:mail_id>/', views.delete_mail, name='delete_mail'),
    path('logout/',views.logout_user, name='logout'),
  
    path('studentRegister/<str:admin_username>/',views.studentRegister, name='studentRegister' ),
    path('facultyRegister/<str:admin_username>',views.facultyRegister, name='facultyRegister' ),
    path('adminLogin/', views.adminLogin, name='adminLogin' ),
    path('adminPage/<str:admin_username>/', views.adminPage, name='adminPage'),
    path('assign/<str:admin_username>/', views.assign, name='assign'),
    path('admin/', admin.site.urls, name='admin' ),
    path('predict/<str:admin_username>/', views.predict, name='predict' ),
    path('units/<str:admin_username>/', views.units, name='units' ),

]