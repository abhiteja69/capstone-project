from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from .views import VerificationView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt



urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('login/', views.user_login, name='login'),
    
    path('password_reset.html', views.password_reset_request, name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html", success_url = '/accounts/reset/done'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),      

    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name='password_reset_complete'),

    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('settings/<int:pk>', views.AccountSettings.as_view(), name='settings'),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
]
