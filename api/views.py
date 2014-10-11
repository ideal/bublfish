# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    return JsonResponse(data = {'我们': '呵呵'}, content_type = 'application/json; charset=utf-8')
