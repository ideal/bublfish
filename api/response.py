# -*- encoding: utf-8 -*-

from django.http import HttpResponse
from django.http import JsonResponse

DATA_OK  = {'status': 200,
            'data': {}
           }
DATA_ERR = {'status': 500,
            'data': {},
            'info': '',
           }

CONTENT_TYPE_JSON = 'application/json; charset=utf-8'

KWARGS_JSON = {'content_type': CONTENT_TYPE_JSON}

def error(status_code, status_msg, is_json=True):
    if not is_json:
        return HttpResponse(content=status_msg, status=status_code)

    data = DATA_ERR
    data['status'] = status_code
    data['info']   = status_msg
    return JsonResponse(data, **KWARGS_JSON)

