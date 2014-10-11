# -*- encoding: utf-8 -*-

import logging

from django.shortcuts import render
from django.http import JsonResponse

from comment.views import CONTENT_TYPE_JSON
from comment.views import DATA_OK
from comment.views import DATA_ERR

log = logging.getLogger(__name__)

def index(request):
    return JsonResponse(data = DATA_OK, content_type = CONTENT_TYPE_JSON)
