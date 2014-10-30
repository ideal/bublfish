# -*- encoding: utf-8 -*-
#
# Copyright (C) 2014 Shang Yuanchun <idealities@gmail.com>
#

import copy
import logging

from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

import bublfish.settings as settings
from account.models import User
from api.response import JsonpResponse
from api.response import CONTENT_TYPE_JSON
from api.response import KWARGS_JSON
from api.response import DATA_OK
from api.response import DATA_ERR
from api.request  import login_required, post_required

from api.models import Comment

try:
    import urlparse
except:
    import urllib.parse as urlparse

log = logging.getLogger(__name__)

def index(request):
    return JsonResponse(data = DATA_OK, **KWARGS_JSON)

def pull(request):
    """
    Request: url=http://foo.bar.com&page=1&limit=10

    Response:
    {
        "status": 200,
        "data": [
                {"id": 1, "date": "2014-10-28 18:09:00", "content": "呵呵", "parent": 0, "author": "ideal", "avatar": "http://"},
                {"id": 2, "date": "2014-10-28 18:10:00", "content": "哈哈", "parent": 0, "author": "ideal", "avatar": "http://"},
                ],
    }
    """
    referer = _parse_url(request.META.get('HTTP_REFERER'))
    pageurl = _parse_url(request.GET.get('url'))

    if (referer and pageurl) and (referer['host'] != pageurl['host']):
        from . import response
        return response.error(403, _('Wrong request'), request.GET.get('callback'))

    url = pageurl['url'] if pageurl else (referer['url'] if referer else None)
    if url is None:
        from . import response
        return response.error(400, _('Wrong parameters'), request.GET.get('callback'))

    data = copy.deepcopy(DATA_OK)
    data['data'] = []
    comments = Comment.objects.filter(comment_page=url).order_by('-comment_date')
    for comment in comments:
        user = User.objects.get(id=comment.user_id)
        data['data'].append({
                "id": comment.comment_id,
                "date": timezone.localtime(comment.comment_date).strftime("%Y-%m-%d %H:%M:%S"),
                "content": comment.comment_content,
                "parent": comment.comment_parent,
                "author": user.username,
                "avatar": user.avatar,
                })
    return JsonpResponse(data = data, callback = request.GET.get('callback'),
               content_type = CONTENT_TYPE_JSON)

@post_required
@login_required
def post(request):
    """
    Request:
    {
     "page": "http://foo.bar.com/blog/page/1",
     "content": "Hello, 来自三体世界的评论",
     "parent" : 0,
    }
    """
    comment = Comment()
    comment.user_id = request.user.id
    comment.comment_date = timezone.now()
    comment.comment_page = _parse_url(request.POST.get('page'))['url']
    comment.comment_content = request.POST.get('content')
    if request.POST.get('parent', None):
        try:
            comment.comment_parent = int(request.POST.get('parent'))
        except:
            comment.comment_type   = Comment.TYPE_NORMAL
        else:
            comment.comment_type   = Comment.TYPE_REPLY

    try:
        comment.clean_fields()
    except ValidationError as e:
        from . import response
        return response.error(400, _('Bad data'),
                              request.POST.get('callback'),
                              inner_data = e.message_dict if settings.DEBUG else None)

    comment.save()
    return JsonpResponse(data = DATA_OK, callback = request.POST.get('callback'),
                         **KWARGS_JSON)

def _parse_url(url):
    """
    """
    if url is None:
        return None
    parsed = urlparse.urlparse(url)
    return {'host': parsed.netloc, 'url': parsed.netloc + parsed.path}
