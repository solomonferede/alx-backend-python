# chats/auth.py

from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class JWTLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            raise serializers.ValidationError("Email and password are required")

        # Authenticate using Django auth
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "user_id": str(user.user_id),
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class JWTLoginView(APIView):
    permission_classes = []          # Allow anyone
    authentication_classes = []      # No auth needed

    def post(self, request):
        serializer = JWTLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
