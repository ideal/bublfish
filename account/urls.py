from django.conf.urls import patterns, url

from account import views

urlpatterns = patterns('',

    url(r'^login/(?P<backend>[^/]+)/$', views.auth,
        name='begin'),
    url(r'^complete/(?P<backend>[^/]+)/$', views.complete,
        name='complete'),
    url(r'^profile/$', views.profile,
        name='profile'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+)/$', views.disconnect,
        name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+)/$',
        views.disconnect, name='disconnect_individual'),
)
