from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, permissions, views
from .serializers import ProfileSerializer
from .models import Profile


class UserProfile(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        user = request.user
        try:
            user_profile = Profile.objects.get(user=user)
            serializer = self.serializer_class(user_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)


class ProfilesList(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'vpn.html'

    def get(self, request):
        user = request.user
        try:
            profile = get_object_or_404(Profile, user=user)
            return Response({'profile': profile})
        except Profile.DoesNotExist:
            return Response({'error_message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
