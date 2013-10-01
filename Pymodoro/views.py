from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User

from Pymodoro.models import Pomodoro

def index(request):
    latest_pomodoro_list = Pomodoro.objects.order_by('-end_time')[:5]
    context = {'latest_pomodoro_list': latest_pomodoro_list}
    return render(request, 'Pymodoro/index.html', context)

def detail(request, pomodoro_id):
    pomodoro = get_object_or_404(Pomodoro, pk=pomodoro_id)
    return render(request, 'Pymodoro/detail.html', {'pomodoro': pomodoro})

def start(request, tag):
    if (request.user.is_authenticated()):
        new_pomodoro = Pomodoro(user=request.user, end_time=timezone.now(), tag=tag)
        new_pomodoro.save()
    return HttpResponseRedirect(reverse('Pymodoro:index'))