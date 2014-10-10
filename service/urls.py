from django.conf.urls import patterns, url

from service import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
)
