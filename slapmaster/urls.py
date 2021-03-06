from django.conf.urls import patterns, url

from slapmaster import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='post_list'),
    url(r'^(?P<pk>\d+)/detail/$', views.DetailView.as_view(), 
        name='post_detail'),
    url(r'^(?P<pk>\d+)/vote/(?P<vote>up|down)$', views.votepost, 
        name='votepost'),
    url(r'^addpost/$', views.addpost, name='addpost'),
    url(r'^addresponse/$', views.addresponse, name='addresponse'),
    url(r'^fb_login/$', views.fb_login, name='fb_login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user_prefs/$', views.UserPrefsView.as_view(), name='user_prefs'),
    url(r'^user_prefs/save$', views.user_prefs_save, name='user_prefs_save'),
)
