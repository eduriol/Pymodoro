from django.test import TestCase

from Pymodoro.models import Pomodoro

import datetime

class PomodoroMethodTests(TestCase):

    def test_init_time(self):
        """
        init_time() should return 25 minutes before end time.
        """
        p = Pomodoro(end_time=datetime.datetime(2000, 1, 1, 0, 0, 0, 0))
        self.assertEqual(p.init_time(), datetime.datetime(1999, 12, 31, 23, 35, 0, 0))

    def test_is_from_today_with_past_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from before today.
        """
        p = Pomodoro(end_time=datetime.datetime.today() - datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)

    def test_is_from_today_with_today_pomodoro(self):
        """
        is_from_today() should return true if the pomodoro is from today.
        """
        p = Pomodoro(end_time=datetime.datetime.today())
        self.assertEqual(p.is_from_today(), True)

    def test_is_from_today_with_future_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from after today.
        """
        p = Pomodoro(end_time=datetime.datetime.today() + datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)