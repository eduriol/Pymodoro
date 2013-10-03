from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic
import time

from Pymodoro.models import Pomodoro, PomodoroManager

class IndexView(generic.ListView):
    template_name = 'Pymodoro/index.html'
    context_object_name = 'today_pomodoro_list'

    def get_queryset(self):
        # Return the pomodoros published today.
        pm = PomodoroManager()
        return pm.are_from_today()

class DetailView(generic.DetailView):
    model = Pomodoro
    template_name = 'Pomodoro/detail.html'

def start(request):
    if (request.user.is_authenticated()):
        time.sleep(1*1) # minutes * seconds/minute
        new_pomodoro = Pomodoro(user=request.user, end_time=timezone.now(), tag=request.POST['tag'])
        new_pomodoro.save()
    return HttpResponseRedirect(reverse('Pymodoro:index'))