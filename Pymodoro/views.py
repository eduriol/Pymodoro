from django.shortcuts import render
from django.http import HttpResponse

from Pymodoro.models import Pomodoro

def index(request):
    latest_pomodoro_list = Pomodoro.objects.order_by('-end_time')[:5]
    output = ', '.join([p.__unicode__() for p in latest_pomodoro_list])
    return HttpResponse(output)

def detail(request, pomodoro_id):
    return HttpResponse("You're looking at pomodoro %s." % pomodoro_id)