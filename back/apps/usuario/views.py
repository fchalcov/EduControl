from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UsuarioSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_usuario(request):

    usuarios = User.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)

    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuario(request):

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({
            "success": False,
            "message": "Username y password son requeridos"
        }, status=400)
    
    user_obj = User.objects.filter(username=username).first()

    if user_obj is None:
        return Response({
            "success": False,
            "message": "Credenciales inválidas"
        }, status=401)

    if not user_obj.is_active:
        return Response({
            "success": False,
            "message": "Usuario inactivo"
        }, status=403)

    user = authenticate(username=username, password=password)

    if user is None:
        return Response({
            "success": False,
            "message": "Credenciales inválidas, verifica tu usuario y contraseña"
        }, status=401)

    refresh = RefreshToken.for_user(user)
    serializer = UsuarioSerializer(user)

    return Response({
        "success": True,
        "user": serializer.data,
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)