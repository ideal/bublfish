# -*- encoding: utf-8 -*-

from django.http import JsonResponse

from api.response import DATA_OK
from api.response import CONTENT_TYPE_JSON

def index(request):
    """
    Default index page.
    """
    return JsonResponse(data = DATA_OK,
               content_type = CONTENT_TYPE_JSON)
