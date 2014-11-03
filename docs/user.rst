User
====

User login
----------

Path: ``/login/<backend>/`` (backend e.g. ``github``, ``douban-oauth2``, ``weibo``)

Method: GET

Request::

    None

Response::

    {
        "status": 200,
        "data": {
            "url": "http://www.douban.com/service/auth2/auth?client_id=1986..."
        }
    }

User profile
------------

Path: ``/profile/``

Method: GET

Request::

    None

Response::

    {
        "status": 200,
        "data": {
            "username": "ideal",
            "avatar": "http://mirror.bjtu.edu.cn"
        }
    }

    If not logined:

    {
        "status": 403,
        "data": {},
        "info": "Need login"
    }
