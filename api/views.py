# -*- encoding: utf-8 -*-

import logging

from django.shortcuts import render
from django.http import JsonResponse

from api.response import JsonpResponse
from api.response import CONTENT_TYPE_JSON
from api.response import KWARGS_JSON
from api.response import DATA_OK
from api.response import DATA_ERR
from api.request  import login_required

from api.models import Comment

try:
    import urlparse
except:
    import urllib.parse as urlparse

log = logging.getLogger(__name__)

def index(request):
    return JsonResponse(data = DATA_OK, **KWARGS_JSON)

def pull(request):
    referer = _parse_url(request.META.get('HTTP_REFERER'))
    page    = _parse_url(request.GET.get('page'))

    if (referer and page) and (referer['host'] != page['host']):
        from . import response
        return response.error(403, 'Wrong request', request.GET.get('callback'))

    url = page['url'] if page else (referer['url'] if referer else None)
    if url is None:
        from . import response
        return response.error(400, 'Wrong parameters', request.GET.get('callback'))

    return JsonpResponse(data = DATA_OK, callback = request.GET.get('callback'),
               content_type = CONTENT_TYPE_JSON)

@login_required()
def post(request):
    if request.method != 'POST':
        from . import response
        return response.error(405, 'Wrong method', request.GET.get('callback'))

    comment = Comment()
    return JsonpResponse(data = DATA_OK, callback = request.POST.get('callback'),
                         **KWARGS_JSON)

def _parse_url(url):
    """
    """
    if url is None:
        return None
    parsed = urlparse.urlparse(url)
    return {'host': parsed.netloc, 'url': parsed.netloc + parsed.path}
