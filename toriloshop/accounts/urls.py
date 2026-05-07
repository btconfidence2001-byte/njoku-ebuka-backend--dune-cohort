from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns =[
    # Djangos built-in login view - handles both GET (show form) and POST (process form) requests
    path('accounts/login/' , auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),

    # Logout view - uses Django's built-in LogoutView, which handles logout logic and redirects to LOGOUT_REDIRECT_URL
    path('accounts/logout/' , auth_views.LogoutView.as_view(), name='logout'),

    # custom registration view
    path('accounts/register/' ,views.register, name='register'),

    # Dashboard view - only accessible to logged in users
    path('dashboard/', views.dashboard, name='dashboard'),
]