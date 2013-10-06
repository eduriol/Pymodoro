from django.conf.urls import patterns, url

from Pymodoro import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^tag/(?P<tag>[a-z]*)/$', views.tag, name='tag'),
    url(r'^start/$', views.start, name='start'),
)