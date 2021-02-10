import os
import uuid
from django.conf import settings


def get_api_url(name='api', version=settings.API_VERSION, app_name='', url_name=''):
    url = '{0}/{1}/'.format(name, version)

    if app_name and url_name:
        url = '{0}{1}/{2}/'.format(url, app_name, url_name)

    elif app_name and not url_name:
        url = '{0}{1}/'.format(url, app_name)

    elif url_name and not app_name:
        url = '{0}{1}/'.format(url, url_name)

    return url


def get_unique_file_name(name):
    return str(uuid.uuid4()) + os.path.splitext(os.path.basename(name))[1]

