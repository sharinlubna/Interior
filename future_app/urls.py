from django.urls import path
from . import views

urlpatterns =[
    path('', views.Home, name='home'),
    path('about', views.About, name='about'),
    path('blog', views.Blog, name='blog'),
    path('blog_detail', views.Blog_Detail, name='blog_detail'),
    path('contact', views.Contact, name='contact'),
    path('team', views.Team, name='team'),
    path('team_detail', views.Team_Detail, name='team_detail'),
    path('user_login', views.user_login, name='user_login'),
    path('UserLoginPage', views.UserLoginPage, name='UserLoginPage'),
    path('logout', views.Logout, name='logout'),
    path('AdminDashboard', views.AdminDashboard, name='AdminDashboard'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('edit_staff/<int:staff_id>', views.edit_staff, name='edit_staff'),
    path('delete_staff/<int:staff_id>', views.delete_staff, name='delete_staff'),

    path('appointment/', views.appointment, name='appointment'),
]