# -*- encoding: utf-8 -*-

from django.http import JsonResponse

JSON_CONTENT_TYPE = 'application/json; charset=utf-8'

def index(request):
    return JsonResponse(data = {'status': 200, 'data': {}},
               content_type = JSON_CONTENT_TYPE)
