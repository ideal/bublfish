from django.conf.urls import patterns, include, url
#from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'bublfish.views.index', name='index'),
    url(r'^comment/', include('api.urls')),
    url('', include('social.apps.django_apps.urls', namespace='social')),
)
