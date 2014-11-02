from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bublfish.views.index', name='index'),
    url(r'^comment/', include('api.urls')),
    url('', include('account.urls', namespace='social')),
)

import api.views
handler500 = api.views.view_500
