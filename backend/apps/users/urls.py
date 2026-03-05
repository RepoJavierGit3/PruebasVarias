from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user-register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('profile/settings/', views.UserProfileSettingsView.as_view(), name='user-profile-settings'),
    path('settings/', views.UserSettingsView.as_view(), name='user-settings'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('stats/', views.user_stats, name='user-stats'),
    path('upload-avatar/', views.upload_avatar, name='upload-avatar'),
]
