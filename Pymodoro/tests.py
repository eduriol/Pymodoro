from django.contrib.auth.models import User
from django.utils.timezone import utc

from Pymodoro.models import Pomodoro, PomodoroManager

import datetime, unittest

class PomodoroMethodTests(unittest.TestCase):

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

class PomodoroManagerMethodTests(unittest.TestCase):

    def test_are_from_today_with_two_past_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the past.
        """
        u1 = User(username='john_doe')
        u1.save()
        u2 = User(username='jane_doe')
        u2.save()
        p1 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        p1.save()
        p2 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=2))
        p2.save()
        p3 = Pomodoro(user=u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p3.save()
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 0)
        u1.delete()
        u2.delete()

    def test_are_from_today_with_a_past_pomodoro_and_a_today_pomodoro_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with only the today's pomodoro.
        """
        u1 = User(username='john_doe')
        u1.save()
        u2 = User(username='jane_doe')
        u2.save()
        p1 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        p1.save()
        p2 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p2.save()
        p3 = Pomodoro(user=u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p3.save()
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 1)
        self.assertIn(p2, pm.are_from_today(u1))
        u1.delete()
        u2.delete()

    def test_are_from_today_with_two_today_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with both pomodoros.
        """
        u1 = User(username='john_doe')
        u1.save()
        u2 = User(username='jane_doe')
        u2.save()
        p1 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p1.save()
        p2 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p2.save()
        p3 = Pomodoro(user=u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p3.save()
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 2)
        self.assertIn(p1, pm.are_from_today(u1))
        self.assertIn(p2, pm.are_from_today(u1))
        u1.delete()
        u2.delete()

    def test_are_from_today_with_a_today_pomodoro_and_a_future_pomodoro_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with only the today's pomodoro.
        """
        u1 = User(username='john_doe')
        u1.save()
        u2 = User(username='jane_doe')
        u2.save()
        p1 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p1.save()
        p2 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        p2.save()
        p3 = Pomodoro(user=u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p3.save()
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 1)
        self.assertIn(p1, pm.are_from_today(u1))
        u1.delete()
        u2.delete()

    def test_are_from_today_with_two_future_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the future.
        """
        u1 = User(username='john_doe')
        u1.save()
        u2 = User(username='jane_doe')
        u2.save()
        p1 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        p1.save()
        p2 = Pomodoro(user=u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=2))
        p2.save()
        p3 = Pomodoro(user=u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        p3.save()
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 0)
        u1.delete()
        u2.delete()