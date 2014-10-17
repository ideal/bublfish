# -*- encoding: utf-8 -*-

from functools import wraps
from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.utils.translation import ugettext as _

from api.response import JsonpResponse
from api.response import KWARGS_JSON
from api.response import DATA_ERR
from api.response import error

def login_required(function=None, is_json=True):
    """
    Return a dectorator if ``function`` is None (e.g. @login_required(is_json=True)),
    or call the dectorator if not None (e.g. @login_required).

    """

    dectorator = _login_required_decorator(is_json)
    if function:
        return dectorator(function)
    return dectorator

def _login_required_decorator(is_json):
    """
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated():
                return view_func(request, *args, **kwargs)

            from . import response
            return response.error(403, _('Need login'),
                                  (request.GET.get('callback') if request.method == 'GET' else request.POST.get('callback')),
                                  is_json)

        return _wrapped_view

    return decorator

def post_required(view_func):
    """
    """

    @wraps(view_func, assigned=available_attrs(view_func))
    def _wrapped_view(request, *args, **kwargs):
        if request.method != 'POST':
            from . import response
            return response.error(405, _('Wrong method'), request.GET.get('callback'))

        return view_func(request, *args, **kwargs)
    return _wrapped_view
