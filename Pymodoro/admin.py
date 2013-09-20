from django.contrib import admin
from Pymodoro.models import Pomodoro

class PomodoroAdmin(admin.ModelAdmin):
    fields = ['user', 'end_time', 'tag']

admin.site.register(Pomodoro, PomodoroAdmin)
