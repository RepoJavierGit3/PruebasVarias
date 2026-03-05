from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('health/', views.HealthCheckView.as_view(), name='health-check'),
    path('system-info/', views.system_info, name='system-info'),
    path('configurations/', views.configurations, name='configurations'),
    path('audit-logs/', views.audit_logs, name='audit-logs'),
]
