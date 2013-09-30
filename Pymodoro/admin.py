from django.contrib import admin
from Pymodoro.models import Pomodoro

class PomodoroAdmin(admin.ModelAdmin):
    fields = ['user', 'end_time', 'tag']
    list_display = ('id', 'user', 'tag', 'init_time', 'end_time', 'is_from_today')
    list_filter = ['end_time']
    search_fields = ['tag']
    date_hierarchy = 'end_time'

admin.site.register(Pomodoro, PomodoroAdmin)