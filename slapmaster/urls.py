from django.conf.urls import patterns, url

from slapmaster import views

urlpatterns = patterns('',
        url(r'^$', views.allposts, name='allposts'),
        url(r'^post/', views.post, name='post'),
        )
