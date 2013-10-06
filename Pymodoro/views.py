from django.shortcuts import render, get_list_or_404
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
        return pm.are_from_today(self.request.user)

class DetailView(generic.DetailView):
    model = Pomodoro
    template_name = 'Pymodoro/detail.html'

    def get_queryset(self):
        # Excludes any pomodoros from other user.
        return Pomodoro.objects.filter(user=self.request.user)

def tag(request, tag):
    pomodoro_list = get_list_or_404(Pomodoro, user=request.user, tag=tag)
    return render(request, 'Pymodoro/tag.html', {'pomodoro_list': pomodoro_list})

def start(request):
    if (request.user.is_authenticated()):
        time.sleep(1*1) # minutes * seconds/minute
        new_pomodoro = Pomodoro(user=request.user, end_time=timezone.now(), tag=request.POST['tag'])
        new_pomodoro.save()
    return HttpResponseRedirect(reverse('Pymodoro:index'))