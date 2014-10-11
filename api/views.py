# -*- encoding: utf-8 -*-

import logging

from django.shortcuts import render
from django.http import JsonResponse

from api.response import CONTENT_TYPE_JSON
from api.response import KWARGS_JSON
from api.response import DATA_OK
from api.response import DATA_ERR

log = logging.getLogger(__name__)

def index(request):
    return JsonResponse(data = DATA_OK, **KWARGS_JSON)

def pull(request):
    return JsonResponse(data = DATA_ERR,
               content_type = CONTENT_TYPE_JSON)

def post(request):
    if request.method != 'POST':
        from . import response
        return response.error(405, 'Wrong method')

    return JsonResponse(data = DATA_OK, **KWARGS_JSON)
