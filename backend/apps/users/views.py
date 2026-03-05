from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import User, UserProfile, UserSettings
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    UserProfileSerializer, UserSettingsSerializer, PasswordChangeSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Usuario registrado exitosamente'
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    
    # Update last login and IP
    user.last_login = timezone.now()
    user.last_login_ip = request.META.get('REMOTE_ADDR')
    user.save(update_fields=['last_login', 'last_login_ip'])
    
    # Login the user
    login(request, user)
    
    # Create or get token
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        'user': UserSerializer(user).data,
        'token': token.key,
        'message': 'Login exitoso'
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    try:
        # Delete the token
        request.user.auth_token.delete()
    except:
        pass
    
    # Logout the user
    logout(request)
    
    return Response({'message': 'Sesión cerrada correctamente'})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfileSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


class UserSettingsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        settings, created = UserSettings.objects.get_or_create(user=self.request.user)
        return settings


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def change_password_view(request):
    serializer = PasswordChangeSerializer(
        data=request.data,
        context={'request': request}
    )
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    user.set_password(serializer.validated_data['new_password'])
    user.save()
    
    # Delete old token to force re-login
    try:
        user.auth_token.delete()
    except:
        pass
    
    return Response({'message': 'Contraseña actualizada correctamente'})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_stats(request):
    """
    Get user statistics
    """
    user = request.user
    return Response({
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'is_verified': user.is_verified,
        'profile_completion': self._calculate_profile_completion(user)
    })
    
    def _calculate_profile_completion(self, user):
        """
        Calculate profile completion percentage
        """
        fields = ['first_name', 'last_name', 'phone', 'bio', 'website', 'location']
        completed = sum(1 for field in fields if getattr(user, field))
        return round((completed / len(fields)) * 100, 0)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def upload_avatar(request):
    """
    Upload user avatar
    """
    user = request.user
    avatar = request.FILES.get('avatar')
    
    if not avatar:
        return Response(
            {'error': 'No se proporcionó ninguna imagen'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file type
    if not avatar.content_type.startswith('image/'):
        return Response(
            {'error': 'El archivo debe ser una imagen'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate file size (5MB max)
    if avatar.size > 5 * 1024 * 1024:
        return Response(
            {'error': 'La imagen no puede ser mayor a 5MB'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user.avatar = avatar
    user.save()
    
    return Response({
        'message': 'Avatar actualizado correctamente',
        'avatar_url': user.get_avatar_url()
    })
