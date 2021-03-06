# -*- encoding: utf-8 -*-

import copy
import logging

from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST

from social.actions import do_auth, do_complete, do_disconnect
from social.apps.django_app.utils import psa

import api.request
from api.response import JsonpResponse
from api.response import DATA_OK

log = logging.getLogger(__name__)

@psa('social:complete')
def auth(request, backend):
    # return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)
    data = copy.deepcopy(DATA_OK)
    data['data']['url'] = request.backend.auth_url()
    return JsonpResponse(data, callback = request.GET.get('callback'))

@csrf_exempt
@psa('social:complete')
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, *args, **kwargs)

@csrf_exempt
@api.request.login_required
def logout_(request):
    """
    """
    logout(request)
    return JsonpResponse(DATA_OK, callback = request.GET.get('callback'))

@api.request.login_required
def profile(request):
    data = copy.deepcopy(DATA_OK)
    data['data']['username'] = request.user.username;
    data['data']['avatar']   = request.user.avatar;
    return JsonpResponse(data, callback = request.GET.get('callback'))

@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(request.backend, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)


def _do_login(backend, user, social_user):
    user.backend = '{0}.{1}'.format(backend.__module__,
                                  backend.__class__.__name__)
    login(backend.strategy.request, user)
    if backend.setting('SESSION_EXPIRATION', False):
        # Set session expiration date if present and enabled
        # by setting. Use last social-auth instance for current
        # provider, users can associate several accounts with
        # a same provider.
        expiration = social_user.expiration_datetime()
        if expiration:
            try:
                backend.strategy.request.session.set_expiry(
                    expiration.seconds + expiration.days * 86400
                )
            except OverflowError:
                # Handle django time zone overflow
                backend.strategy.request.session.set_expiry(None)
