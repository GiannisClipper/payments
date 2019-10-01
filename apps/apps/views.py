from django.http import HttpResponse

from apps.constants import WELCOME, SIGNATURE, LINKEDIN_URL, GITHUB_URL

content = f'''
{WELCOME}
........................................
Available API requests:
/ GET (root)
........................................
{SIGNATURE}
{LINKEDIN_URL}
{GITHUB_URL}
'''


def root(req):
    return HttpResponse(content, content_type="text/plain")
