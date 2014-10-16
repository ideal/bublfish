#
# Copyright (C) 2014 Shang Yuanchun <idealities@gmail.com>
#

import hashlib
import requests
import logging

GRAVATAR_PREFIX      = 'http://www.gravatar.com/avatar/'
DEFAULT_GRAVATAR_URL = GRAVATAR_PREFIX + '00000000000000000000000000000000?d=mm&s=200'

log = logging.getLogger(__name__)

def make_default_avatar(email):
    """
    """

    digest = hashlib.md5(
                 email.strip().lower()).hexdigest()
    gravatar = GRAVATAR_PREFIX + digest + '?s=200'
    try:
        # for 400ms
        response = requests.head(gravatar, timeout=0.4)
    except:
        log.info('http request error, url:%s', gravatar)
        return DEFAULT_GRAVATAR_URL

    return gravatar if response.status_code == 200 else DEFAULT_GRAVATAR_URL

