from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('sw.js', views.service_worker, name='service_worker'),
    path('api/pwa-version/', views.pwa_version, name='pwa_version'),
    path('', views.home, name='dashboard_home'),
]
