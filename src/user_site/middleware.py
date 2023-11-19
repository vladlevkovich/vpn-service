from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .models import Site
import uuid


class ModifyLinksMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.site_id = None

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the response contains HTML content
        if response.get('Content-Type', '').startswith('text/html'):
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the site ID from the request path
            site_url = request.path.split('/')
            site_id = site_url[5]
            try:
                site = Site.objects.get(id=uuid.UUID(site_id))

                modified_links = []
                data = soup.find_all('a')

                for tag in data:
                    if 'href' in tag.attrs:
                        domain = urlparse(site.url).netloc
                        internal_route = f'{site.name}/{domain}'

                        href = tag['href']
                        is_external = href.startswith('http://') or href.startswith('https://')

                        if not is_external and site.url in href:
                            # If it's an internal link
                            internal_path = urlparse(href).path
                            new_link = f'{internal_route}{internal_path}'
                            modified_links.append((tag['href'], new_link))
                            tag['href'] = new_link
                        elif is_external:
                            # If it's an external link
                            tag['href'] = f'https://{internal_route}'
            except Site.DoesNotExist:
                print('Site not found')

            response.content = str(soup)

        return response
