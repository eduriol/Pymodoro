# coding=utf-8

from django.conf.urls import patterns, url

from Pymodoro import views

urlpatterns = patterns('',
    #url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^tag/(?P<tag>[\w|\W]*)/$', views.tag, name='tag'),
    url(r'^logout/$', views.logoutView, name='logout'),
)