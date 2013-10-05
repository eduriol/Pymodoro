from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.test import TestCase

from Pymodoro.models import Pomodoro, PomodoroManager

import datetime, unittest

def create_user(username='john_doe'):
    return User.objects.create(username=username)

def create_pomodoro(user, end_time, tag='foo'):
        return Pomodoro.objects.create(user=user, end_time=end_time, tag=tag)

class PomodoroMethodTests(unittest.TestCase):

    def test_init_time(self):
        """
        init_time() should return 25 minutes before end time.
        """
        u = create_user()
        dt = datetime.datetime.utcnow().replace(tzinfo=utc)
        p = create_pomodoro(u, dt)
        self.assertEqual(p.init_time(), dt - datetime.timedelta(minutes=25))
        u.delete()

    def test_is_from_today_with_past_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from before today.
        """
        u = create_user()
        p = create_pomodoro(u, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)
        u.delete()

    def test_is_from_today_with_today_pomodoro(self):
        """
        is_from_today() should return true if the pomodoro is from today.
        """
        u = create_user()
        p = create_pomodoro(u, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(p.is_from_today(), True)
        u.delete()

    def test_is_from_today_with_future_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from after today.
        """
        u = create_user()
        p = create_pomodoro(u, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)
        u.delete()

class PomodoroManagerMethodTests(unittest.TestCase):

    def test_are_from_today_with_two_past_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the past.
        """
        u1 = create_user('john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=2))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 0)
        u1.delete()
        u2.delete()

    def test_are_from_today_with_a_past_pomodoro_and_a_today_pomodoro_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with only the today's pomodoro.
        """
        u1 = create_user('john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        p2 = create_pomodoro(u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 1)
        self.assertIn(p2, pm.are_from_today(u1))
        u1.delete()
        u2.delete()

    def test_are_from_today_with_two_today_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with both pomodoros.
        """
        u1 = create_user('john_doe')
        u2 = create_user('jane_doe')
        p1 = create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        p2 = create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
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
        u1 = create_user('john_doe')
        u2 = create_user('jane_doe')
        p1 = create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 1)
        self.assertIn(p1, pm.are_from_today(u1))
        u1.delete()
        u2.delete()

    def test_are_from_today_with_two_future_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the future.
        """
        u1 = create_user('john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=2))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        pm = PomodoroManager()
        self.assertEqual(len(pm.are_from_today(u1)), 0)
        u1.delete()
        u2.delete()

class PomodoroIndexViewTests(TestCase):

    def test_index_view_with_no_pomodoros_from_anybody(self):
        """
        If no pomodoros exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])

    def test_index_view_with_no_pomodoros_from_user_and_pomodoros_from_other_user_from_past_and_future(self):
        """
        If no pomodoros from current user exist, an appropriate message should be displayed.
        """
        u1 = create_user('john_doe')
        self.client.login(username='john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])
        u1.delete()
        u2.delete()

    def test_index_view_with_no_pomodoros_from_user_and_pomodoros_from_other_user_from_today(self):
        """
        If no pomodoros from current user exist, an appropriate message should be displayed.
        """
        u1 = create_user('john_doe')
        self.client.login(username='john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])
        u1.delete()
        u2.delete()

    def test_index_view_with_one_pomodoro_from_user_from_past_and_future_and_pomodoros_from_other_user_from_today(self):
        """
        If no pomodoros from today from current user exist, an appropriate message should be displayed.
        """
        u1 = create_user('john_doe')
        self.client.login(username='john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])
        u1.delete()
        u2.delete()

    def test_index_view_with_one_pomodoro_from_user_from_today_and_pomodoros_from_other_user_from_today(self):
        """
        If a pomodoro from today from current user exists, an appropriate message should be displayed.
        """
        u1 = create_user('john_doe')
        self.client.login(username='john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 1 pomodoro so far today.", status_code=200)
        self.assertEqual(len(response.context['today_pomodoro_list']), 1)
        u1.delete()
        u2.delete()

    def test_index_view_with_more_than_one_pomodoro_from_user_from_today_and_pomodoros_from_other_user_from_today(self):
        """
        If pomodoros from today from current user exist, an appropriate message should be displayed.
        """
        u1 = create_user('john_doe')
        self.client.login(username='john_doe')
        u2 = create_user('jane_doe')
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 2 pomodoros so far today.", status_code=200)
        self.assertEqual(len(response.context['today_pomodoro_list']), 2)
        u1.delete()
        u2.delete()
