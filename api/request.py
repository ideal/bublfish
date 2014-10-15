# -*- encoding: utf-8 -*-

from functools import wraps
from django.http import HttpResponse
from django.utils.decorators import available_attrs

from api.response import JsonpResponse
from api.response import KWARGS_JSON
from api.response import DATA_ERR

def login_required(is_json=True):
    """
    """

    return _login_required_decorator(is_json)

def _login_required_decorator(is_json):
    """
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)

            status_code = 403
            status_msg  = 'Need login'
            if not is_json:
                return HttpResponse(content=status_msg, status=status_code)

            data = DATA_ERR
            data['status'] = status_code
            data['info']   = status_msg
            return JsonpResponse(data, request.POST.get('callback'), **KWARGS_JSON)

        return _wrapped_view

    return decorator

