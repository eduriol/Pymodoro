from django.conf.urls import patterns, url

from Pymodoro import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<pomodoro_id>\d+)/$', views.detail, name='detail'),
)