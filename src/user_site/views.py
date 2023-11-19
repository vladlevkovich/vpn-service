from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status, views
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from django.conf import settings
from .serializers import *
from .models import *
import requests


class SitesList(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CreateSiteSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        try:
            user_profile = Profile.objects.get(user=request.user)
            sites = Site.objects.filter(user=user_profile)
            serializer = self.serializer_class(sites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'message': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user_profile = Profile.objects.get(user=request.user)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user_profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProxySite(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'links.html'

    def get(self, request, site_id):
        try:
            user_profile = Profile.objects.get(user=request.user)
            site = Site.objects.get(id=site_id)
            # url = f'{site.url}/{path}'
            # SiteVist.objects.create(site=site)
            if site.user == user_profile:

                proxies = {
                    'http': settings.HTTP,
                    'https': settings.HTTPS
                }

                try:
                    # external_url = site.url + request.get_full_path()
                    external_url = site.url + request.path
                    response = requests.get(external_url, proxies=proxies)
                    print(response.content)
                    print(request.body)
                    TrafficStatic.objects.create(
                        site=site,
                        path=request.path,
                        incoming_traffic=len(response.content),
                        outgoing_traffic=len(request.body)
                    )
                    # url = reverse('proxy-site', args=[site_id])
                    context = {
                        'url': site.url
                    }
                    return Response(context, status=status.HTTP_200_OK)
                except requests.exceptions.RequestException as e:
                    return Response({'error': str(e)})
                # return HttpResponse(response, status=status.HTTP_200_OK)
        except Site.DoesNotExist:
            return Response({'message': 'Site not found'}, status=status.HTTP_404_NOT_FOUND)
