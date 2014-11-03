Comment
=======

Retrive comments
----------------

Path: ``/comment/pull``

Method: GET

Request::

    {
        "url": "http://caifu.baidu.com/insurance/page/1",
        "page": 1,
        "limit": 10
    }

Response::

    {
        "status": 200,
        "data": [
            {"id": 1, "date": "2014-10-20 18:09:00", "content": "呵呵", "parent": 0,
             "author": "ideal", "avatar": "http://mirror.bjtu.edu.cn/icon.jpg",
             "ups": 0, "downs": 0},
            {"id": 2, "date": "2014-10-20 18:00:00", "content": "哈哈", "parent": 0,
             "author": "ideal", "avatar": "http://mirror.bjtu.edu.cn/icon.jpg"
             "ups": 0, "downs": 0}
        ]
    }


Post comment
------------

Path: ``/comment/post``

Method: POST

Request::

    {
        "page": "http://foo.bar.com/blog/page/1",
        "content": "三体世界向你问好",
        "parent": 0
    }

Response::

    {
        "status": 200,
        "data": {}
    }

Delete comment
--------------

Path: ``/comment/delete``

Method: POST

Request::

    {
        "id": 1986
    }

Response::

    {
        "status": 200,
        "data": {}
    }

Update comment
--------------

Path: ``/comment/update``

Method: POST

Request::

    {
        "id": 1986,
        "content": "新大厦好荒凉"
    }

Response::

    {
        "status": 200,
        "data": {}
    }
