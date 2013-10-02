from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
import time

from Pymodoro.models import Pomodoro, PomodoroManager

def index(request):
    latest_pomodoro_list = PomodoroManager.are_from_today()
    context = {'latest_pomodoro_list': latest_pomodoro_list}
    return render(request, 'Pymodoro/index.html', context)

def detail(request, pomodoro_id):
    pomodoro = get_object_or_404(Pomodoro, pk=pomodoro_id)
    return render(request, 'Pymodoro/detail.html', {'pomodoro': pomodoro})

def start(request):
    if (request.user.is_authenticated()):
        time.sleep(1*1) # minutes * seconds/minute
        new_pomodoro = Pomodoro(user=request.user, end_time=timezone.now(), tag=request.POST['tag'])
        new_pomodoro.save()
    return HttpResponseRedirect(reverse('Pymodoro:index'))