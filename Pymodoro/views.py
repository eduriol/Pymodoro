from django.shortcuts import render, get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views import generic

import time

from Pymodoro.models import Pomodoro, PomodoroManager
from Pymodoro.forms import StartForm


def index(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = StartForm(request.POST)
            if form.is_valid():
                time.sleep(1*1) # minutes * seconds/minute
                pomodoro_tag = form.cleaned_data['tag']
                new_pomodoro = Pomodoro(user=request.user, end_time=timezone.now(), tag=pomodoro_tag)
                new_pomodoro.save()
                return HttpResponseRedirect(reverse('Pymodoro:index'))
        else:
            form = StartForm()
        pm = PomodoroManager()
        today_pomodoro_list = pm.are_from_today(request.user)
        return render(request, 'Pymodoro/index.html', {'form': form, 'today_pomodoro_list': today_pomodoro_list})


class DetailView(generic.DetailView):
    model = Pomodoro
    template_name = 'Pymodoro/detail.html'

    def get_queryset(self):
        # Excludes any pomodoros from other user.
        return Pomodoro.objects.filter(user=self.request.user)


def tag(request, tag):
    pomodoro_list = get_list_or_404(Pomodoro, user=request.user, tag=tag)
    return render(request, 'Pymodoro/tag.html', {'pomodoro_list': pomodoro_list})