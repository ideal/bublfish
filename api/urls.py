from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'pull/', views.pull, name='pull'),
    url(r'post/', views.post, name='post'),
)
