from django.contrib import admin
from Pymodoro.models import Pomodoro

class PomodoroAdmin(admin.ModelAdmin):
    fields = ['user', 'end_time', 'tag']
    list_display = ('user', 'tag', 'init_time', 'end_time', 'is_from_today')

admin.site.register(Pomodoro, PomodoroAdmin)