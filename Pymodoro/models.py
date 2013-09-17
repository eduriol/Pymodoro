from django.db import models
from django.contrib.auth.models import User

import datetime

class Pomodoro(models.Model):
    user = models.ForeignKey(User)
    tag = models.CharField(max_length=200)
    end_time = models.DateTimeField("end time")

    def __unicode__(self):
        name = "(%s, %s, %s)" % (self.tag, self.init_time, self.end_time)
        return name

    def init_time(self):
        return self.end_time - datetime.timedelta(minutes=25)

    def is_from_today(self):
        return self.end_time.day == datetime.datetime.today()