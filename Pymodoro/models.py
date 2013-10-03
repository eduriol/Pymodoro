from django.db import models
from django.contrib.auth.models import User

import datetime
from operator import attrgetter

class Pomodoro(models.Model):
    user = models.ForeignKey(User)
    tag = models.CharField(max_length=200)
    end_time = models.DateTimeField("end time")

    def __unicode__(self):
        return 'user %s, from %s to %s in %s' % (self.user.username, self.init_time().strftime('%c'), self.end_time.strftime('%c'), self.tag)

    def init_time(self):
        return self.end_time - datetime.timedelta(minutes=25)

    def is_from_today(self):
        return self.end_time.date() == datetime.date.today()
    is_from_today.admin_order_field = 'end_time'
    is_from_today.boolean = True
    is_from_today.short_description = 'is from today?'

class PomodoroManager(models.Manager):
    def are_from_today(self, user):
        result_list = []
        for p in Pomodoro.objects.all():
            if p.is_from_today() and p.user == user:
                result_list.append(p)
        return sorted(result_list, key=attrgetter('end_time'), reverse=True)