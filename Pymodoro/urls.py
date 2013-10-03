from django.conf.urls import patterns, url

from Pymodoro import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pomodoro_id>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^start/$', views.start, name='start'),
)