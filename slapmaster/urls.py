from django.conf.urls import patterns, url

from slapmaster import views

urlpatterns = patterns('',
        url(r'^$', views.allposts, name='allposts'),
        url(r'^post/(?P<post_id>\d+)/$', views.post, name='post'),
        url(r'^addpost/$', views.addpost, name='addpost'),
        url(r'^addresponse/$', views.addresponse, name='addresponse'),
        )
