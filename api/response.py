# -*- encoding: utf-8 -*-

import copy
import json

from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder

DATA_OK  = {'status': 200,
            'data': {}
           }
DATA_ERR = {'status': 500,
            'data': {},
            'info': '',
           }

CONTENT_TYPE_JSON = 'application/json; charset=utf-8'

KWARGS_JSON = {'content_type': CONTENT_TYPE_JSON}

def error(status_code, status_msg, callback = None, is_json=True, inner_data=None):
    """
    Return a error response, depending on ``is_json``.
    """

    if not is_json:
        return HttpResponse(content=status_msg, status=status_code)

    data = copy.deepcopy(DATA_ERR)
    data['status'] = status_code
    data['info']   = status_msg
    if inner_data:
        data['data'] = inner_data
    return JsonpResponse(data, callback, **KWARGS_JSON)

class JsonpResponse(HttpResponse):
    """
    """
    def __init__(self, data, callback=None, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', CONTENT_TYPE_JSON)
        if data['status'] >= 500:
            kwargs.setdefault('status', data['status'])
        if callback:
            import django.utils.html as html
            callback = html.escape(callback)
        data = ((callback + '(' if callback else '')
                 + json.dumps(data, cls=encoder)
                 + (')' if callback else ''))
        super(JsonpResponse, self).__init__(content=data, **kwargs)

