from django.urls import path
from . import views

urlpatterns =[
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('blog', views.Blog_view, name='blog'),
    path('Blog_Detail/<int:id>', views.Blog_Detail, name='Blog_Detail'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.Team, name='team'),
    path('appointment/', views.appointment, name='appointment'),
    path('subscribe/', views.subscribe, name='subscribe'),

    path('user_login', views.user_login, name='user_login'),
    path('UserLoginPage', views.UserLoginPage, name='UserLoginPage'),
    path('logout', views.Logout, name='logout'),

    path('AdminDashboard', views.AdminDashboard, name='AdminDashboard'),
    path('admin_notification/', views.admin_notification, name='admin_notification'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('edit_staff/<int:staff_id>', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>', views.delete_staff, name='delete_staff'),
    path('create_admin_blog/', views.create_admin_blog, name='create_admin_blog'),
    path('admin_blogs/', views.admin_blogs, name='admin_blogs'),
    path('edit_admin_blog/<int:id>', views.edit_admin_blog, name='edit_admin_blog'),
    path('delete_item/<int:id>', views.delete_item, name='delete_item'),
    path('appointment_list', views.appointment_list, name='appointment_list'),
    path('appointment_view/<int:id>', views.appointment_view, name='appointment_view'),
    path('schedule_appointment/<int:id>', views.schedule_appointment, name='schedule_appointment'),
    path('schedule_app_view/<int:id>', views.schedule_app_view, name='schedule_app_view'),
    path('reject_appointment/<int:id>', views.reject_appointment, name='reject_appointment'),
    path('schedule/<int:id>', views.schedule, name='schedule'),

    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_appointments/', views.staff_appointments, name='staff_appointments'),
    path('staff_app_view/<int:id>', views.staff_app_view, name='staff_app_view'),
    path('staff_reject_appointment/<int:id>', views.staff_reject_appointment, name='staff_reject_appointment'),
    path('staff_blog/', views.staff_blog, name='staff_blog'),
    path('create_staff_blog/', views.create_staff_blog, name='create_staff_blog'),
    path('edit_staff_blog/<int:id>', views.edit_staff_blog, name='edit_staff_blog'),

    path('client_profile/', views.client_profile, name='client_profile'),
    path('design_preference/', views.design_preference, name='design_preference'),
    path('project_updates/', views.project_updates, name='project_updates'),


]