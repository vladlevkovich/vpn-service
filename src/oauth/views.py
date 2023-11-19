from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser
from .serializers import UserRegisterSerializer, UserLoginSerializer
from .authentication import JWTAuthentication


class UserRegister(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CustomUser.objects.filter(email=email)

        if user:
            return Response({'message': 'Such a user exists'}, status=status.HTTP_409_CONFLICT)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserLogin(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        password = serializer.data['password']
        user = CustomUser.objects.get(email=email)
        if not user:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'message': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        access_token = JWTAuthentication.create_access(user)
        refresh_token = JWTAuthentication.create_refresh(user)
        return Response({
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)

