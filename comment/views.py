# -*- encoding: utf-8 -*-

from django.http import JsonResponse

DATA_OK  = {'status': 200,
            'data': {}
           }
DATA_ERR = {'status': 500,
            'data': {},
            'info': '',
           }

CONTENT_TYPE_JSON = 'application/json; charset=utf-8'

def index(request):
    return JsonResponse(data = DATA_OK,
               content_type = CONTENT_TYPE_JSON)
