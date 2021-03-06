# -*- encoding: utf-8 -*-
#
# Copyright (C) 2014 Shang Yuanchun <idealities@gmail.com>
#

import copy
import logging

from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, EmptyPage

import bublfish.settings as settings
from account.models import User
from api.response import JsonpResponse
from api.response import CONTENT_TYPE_JSON
from api.response import KWARGS_JSON
from api.response import DATA_OK
from api.response import DATA_ERR
from api.request  import login_required, post_required
import api.utils

from api.models import Comment

try:
    import urlparse
except:
    import urllib.parse as urlparse

log = logging.getLogger(__name__)

def index(request):
    return JsonResponse(data = DATA_OK, **KWARGS_JSON)

DEFAULT_PAGE_SIZE = 10

class _User(object):
    username = _("anonymous")
    avatar   = api.utils.DEFAULT_GRAVATAR_URL

_user = _User()

def pull(request):
    """
    Request: url=http://foo.bar.com&page=1&limit=10

    Response:
    {
        "status": 200,
        "data": [
                {"id": 1, "date": "2014-10-28 18:09:00", "content": "呵呵",
                 "parent": 0, "author": "ideal", "avatar": "http://"},
                {"id": 2, "date": "2014-10-28 18:10:00", "content": "哈哈",
                 "parent": 0, "author": "ideal", "avatar": "http://"},
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

    def fill_comments(comments):
        for comment in comments:
            try:
                user = User.objects.get(id=comment.user_id)
            except:
                user = _user
            data['data'].append({
                    "id": comment.comment_id,
                    "date": timezone.localtime(comment.comment_date).strftime("%Y-%m-%d %H:%M:%S"),
                    "content": comment.comment_content,
                    "ups": comment.comment_ups,
                    "downs": comment.comment_downs,
                    "parent": comment.comment_parent,
                    "author": user.username,
                    "avatar": user.avatar,
                    })

    # Normal comments
    comments  = Comment.objects.filter(comment_page=url,
                                comment_type=Comment.TYPE_NORMAL).order_by('-comment_date')
    try:
        limit = int(request.GET.get('limit'))
    except:
        limit = DEFAULT_PAGE_SIZE
    try:
        pagenum = int(request.GET.get('page'))
    except:
        pagenum = 1
    limit   = DEFAULT_PAGE_SIZE if limit <= 0 else limit
    pagenum = 1 if pagenum <= 0 else pagenum

    paginator = Paginator(comments, limit)
    try:
        comments  = paginator.page(pagenum)
    except EmptyPage:
        comments = []
    fill_comments(comments)

    # Reply comments
    # TODO: however this will fetch all reply comments.
    comments  = Comment.objects.filter(comment_page=url,
                                comment_type=Comment.TYPE_REPLY).order_by('comment_id')
    fill_comments(comments)

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

    if comment.comment_parent > 0:
        try:
            parent = Comment.objects.get(comment_id=parent)
        except Comment.DoesNotExist:
            from . import response
            return response.error(400, _('Bad data'),
                                  request.POST.get('callback'))

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

@post_required
@login_required
def delete(request):
    """
    Request:
    {
        "id": 1986,
    }
    """
    result = _check_comment(request)
    if isinstance(result, HttpResponse):
        return result

    Comment.objects.filter(comment_id = result).delete()
    return JsonpResponse(data = DATA_OK, callback = request.POST.get('callback'),
                         **KWARGS_JSON)

@post_required
@login_required
def update(request):
    """
    Request:
    {
        "id": 1986,
        "content": "Hello, 来自三体世界的评论",
    }
    """
    result = _check_comment(request)
    if isinstance(result, HttpResponse):
        return result

    if request.POST.get('content'):
        Comment.objects.filter(comment_id = result).update(
                        comment_content = request.POST.get('content'))
    return JsonpResponse(data = DATA_OK, callback = request.POST.get('callback'),
                         **KWARGS_JSON)

@post_required
@login_required
def vote(request):
    """
    Request:
    {
        "id": 1986,
        "action": "up",
    }
    ``action``: up, down
    """
    try:
        cid = int(request.POST.get('id'))
    except:
        from . import response
        return response.error(400, _('Bad data'),
                              request.POST.get('callback'))
    action = request.POST.get('action')
    if not action in ('up', 'down'):
        from . import response
        return response.error(400, _('Bad data'),
                              request.POST.get('callback'))

    # TODO: duplicate vote
    field = (action == 'up' and 'comment_ups' or 'comment_downs')
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute('UPDATE `api_comment` SET `' + field + '`=`' + field + '`+1 WHERE `comment_id`=%s', [cid])
    return JsonpResponse(data = DATA_OK, callback = request.POST.get('callback'),
                         **KWARGS_JSON)


def _check_comment(request):
    """
    """

    from . import response

    try:
        cid = int(request.POST.get('id'))
    except:
        return response.error(400, _('Bad data'),
                              request.POST.get('callback'))

    try:
        comment = Comment.objects.get(comment_id = cid)
    except:
        return response.error(400, _('No such comment'),
                              request.POST.get('callback'))

    if comment.user_id != request.user.id:
        return response.error(400, _('No privileges'),
                              request.POST.get('callback'))

    return cid

def _parse_url(url):
    """
    """
    if url is None:
        return None
    parsed = urlparse.urlparse(url)
    return {'host': parsed.netloc, 'url': parsed.netloc + parsed.path}

def view_500(request):
    """
    """

    import sys
    tp, ex, tb = sys.exc_info()
    log.exception(ex)

    from . import response
    return response.error(500, _('System error'),
           getattr(request, request.method).get('callback'))
