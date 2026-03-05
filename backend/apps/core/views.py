from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Configuration, AuditLog

User = get_user_model()


class HealthCheckView(APIView):
    """
    Health check endpoint for monitoring
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({
            'status': 'healthy',
            'timestamp': timezone.now().isoformat(),
            'version': '1.0.0'
        })


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def system_info(request):
    """
    Get system information
    """
    try:
        user_count = User.objects.count()
        active_users = User.objects.filter(is_active=True).count()
        
        return Response({
            'user_count': user_count,
            'active_users': active_users,
            'server_time': timezone.now().isoformat(),
            'django_version': '4.2.7',
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def configurations(request):
    """
    Get system configurations (admin only)
    """
    configs = Configuration.objects.filter(is_active=True)
    data = {config.key: config.value for config in configs}
    return Response(data)


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def audit_logs(request):
    """
    Get audit logs (admin only)
    """
    logs = AuditLog.objects.all()[:100]  # Last 100 logs
    data = []
    for log in logs:
        data.append({
            'id': log.id,
            'user': log.user.username if log.user else 'Anonymous',
            'action': log.action,
            'model_name': log.model_name,
            'object_repr': log.object_repr,
            'created_at': log.created_at,
            'ip_address': log.ip_address,
        })
    return Response(data)
