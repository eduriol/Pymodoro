from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.core.urlresolvers import reverse
from django.test import TestCase

from Pymodoro.models import Pomodoro, PomodoroManager

import datetime, unittest

def create_user(username='john_doe', password='john_doe'):
    return User.objects.create_user(username=username, password=password)

def create_pomodoro(user, end_time, tag='foo'):
    return Pomodoro.objects.create(user=user, end_time=end_time, tag=tag)

class PomodoroMethodTests(unittest.TestCase):

    def setUp(self):
        self.u = create_user()

    def test_init_time(self):
        """
        init_time() should return 25 minutes before end time.
        """
        dt = datetime.datetime.utcnow().replace(tzinfo=utc)
        p = create_pomodoro(self.u, dt)
        self.assertEqual(p.init_time(), dt - datetime.timedelta(minutes=25))

    def test_is_from_today_with_past_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from before today.
        """
        p = create_pomodoro(self.u, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)

    def test_is_from_today_with_today_pomodoro(self):
        """
        is_from_today() should return true if the pomodoro is from today.
        """
        p = create_pomodoro(self.u, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(p.is_from_today(), True)

    def test_is_from_today_with_future_pomodoro(self):
        """
        is_from_today() should return false if the pomodoro is from after today.
        """
        p = create_pomodoro(self.u, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        self.assertEqual(p.is_from_today(), False)

    def tearDown(self):
        self.u.delete()

class PomodoroManagerMethodTests(unittest.TestCase):

    def setUp(self):
        self.u1 = create_user('john_doe', 'john_doe')
        self.u2 = create_user('jane_doe', 'jane_doe')
        self.pm = PomodoroManager()

    def test_are_from_today_with_two_past_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the past.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=2))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(len(self.pm.are_from_today(self.u1)), 0)

    def test_are_from_today_with_a_past_pomodoro_and_a_today_pomodoro_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with only the today's pomodoro.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        p2 = create_pomodoro(self.u1, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u2, end_time=datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(len(self.pm.are_from_today(self.u1)), 1)
        self.assertIn(p2, self.pm.are_from_today(self.u1))

    def test_are_from_today_with_two_today_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with both pomodoros.
        """
        p1 = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        p2 = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(len(self.pm.are_from_today(self.u1)), 2)
        self.assertIn(p1, self.pm.are_from_today(self.u1))
        self.assertIn(p2, self.pm.are_from_today(self.u1))

    def test_are_from_today_with_a_today_pomodoro_and_a_future_pomodoro_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return a list with only the today's pomodoro.
        """
        p1 = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(len(self.pm.are_from_today(self.u1)), 1)
        self.assertIn(p1, self.pm.are_from_today(self.u1))

    def test_are_from_today_with_two_future_pomodoros_and_a_today_pomodoro_from_other_user(self):
        """
        are_from_today() should return an empty list if all pomodoros are from the future.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=2))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        self.assertEqual(len(self.pm.are_from_today(self.u1)), 0)

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

class PomodoroIndexViewTests(TestCase):

    def setUp(self):
        self.u1 = User.objects.create_user(username='john_doe', password='john_doe')
        self.client.login(username='john_doe', password='john_doe')
        self.u2 = User.objects.create_user(username='jane_doe', password='jane_doe')

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
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])

    def test_index_view_with_no_pomodoros_from_user_and_pomodoros_from_other_user_from_today(self):
        """
        If no pomodoros from current user exist, an appropriate message should be displayed.
        """
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])

    def test_index_view_with_one_pomodoro_from_user_from_past_and_future_and_pomodoros_from_other_user_from_today(self):
        """
        If no pomodoros from today from current user exist, an appropriate message should be displayed.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) - datetime.timedelta(days=1))
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc) + datetime.timedelta(days=1))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 0 pomodoros so far today.", status_code=200)
        self.assertQuerysetEqual(response.context['today_pomodoro_list'], [])

    def test_index_view_with_one_pomodoro_from_user_from_today_and_pomodoros_from_other_user_from_today(self):
        """
        If a pomodoro from today from current user exists, an appropriate message should be displayed.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 1 pomodoro so far today.", status_code=200)
        self.assertEqual(len(response.context['today_pomodoro_list']), 1)

    def test_index_view_with_more_than_one_pomodoro_from_user_from_today_and_pomodoros_from_other_user_from_today(self):
        """
        If pomodoros from today from current user exist, an appropriate message should be displayed.
        """
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:index'))
        self.assertContains(response, "You have completed 2 pomodoros so far today.", status_code=200)
        self.assertEqual(len(response.context['today_pomodoro_list']), 2)

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

class PomodoroDetailViewTests(TestCase):

    def setUp(self):
        self.u1 = create_user('john_doe', 'john_doe')
        self.client.login(username='john_doe', password='john_doe')
        self.u2 = create_user('jane_doe', 'jane_doe')

    def test_detail_view_of_a_non_existent_pomodoro(self):
        """
        The detail view of a pomodoro that does not exist should return a 404 not found.
        """
        response = self.client.get(reverse('Pymodoro:detail', args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_of_an_existent_pomodoro_from_other_user(self):
        """
        The detail view of a pomodoro from other user should return a 404 not found.
        """
        p = create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:detail', args=(p.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_of_an_existent_pomodoro_from_logged_user(self):
        """
        The detail view of a pomodoro from logged user should display correctly.
        """
        p = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc))
        response = self.client.get(reverse('Pymodoro:detail', args=(p.id,)))
        self.assertContains(response, p.id, status_code=200)

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

class PomodoroTagViewTests(TestCase):

    def setUp(self):
        self.u1 = create_user('john_doe', 'john_doe')
        self.client.login(username='john_doe', password='john_doe')
        self.u2 = create_user('jane_doe', 'jane_doe')

    def test_tag_view_of_a_non_existent_tag(self):
        """
        The tag view of a tag that does not exist should return a 404 not found.
        """
        response = self.client.get(reverse('Pymodoro:tag', args=('foo',)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_of_an_existent_tag_from_other_user(self):
        """
        The tag view of a tag from other user should return a 404 not found.
        """
        p = create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        response = self.client.get(reverse('Pymodoro:tag', args=(p.tag,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_of_an_existent_tag_from_logged_user_with_one_pomodoro(self):
        """
        The tag view of a tag from logged user should display correctly.
        """
        p = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        response = self.client.get(reverse('Pymodoro:tag', args=(p.tag,)))
        self.assertContains(response, p.id, status_code=200)
        self.assertEqual(len(response.context['pomodoro_list']), 1)

    def test_detail_view_of_an_existent_tag_from_logged_user_with_two_pomodoros(self):
        """
        The tag view of a tag from logged user should display correctly.
        """
        p1 = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        response = self.client.get(reverse('Pymodoro:tag', args=(p1.tag,)))
        self.assertContains(response, p1.id, status_code=200)
        self.assertEqual(len(response.context['pomodoro_list']), 2)

    def test_detail_view_of_an_existent_tag_from_logged_user_with_same_name_than_other_tag_from_other_user(self):
        """
        The tag view of a tag from logged user should display correctly.
        """
        p1 = create_pomodoro(self.u1, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        create_pomodoro(self.u2, datetime.datetime.utcnow().replace(tzinfo=utc), 'foo')
        response = self.client.get(reverse('Pymodoro:tag', args=(p1.tag,)))
        self.assertContains(response, p1.id, status_code=200)
        self.assertEqual(len(response.context['pomodoro_list']), 1)

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()

class PomodoroStartViewTests(TestCase):

    def setUp(self):
        self.u1 = create_user('john_doe', 'john_doe')
        self.u2 = create_user('jane_doe', 'jane_doe')

    def test_start_view_with_no_user_logged_in(self):
        response = self.client.post(reverse('Pymodoro:start'), {'tag': 'foo'})
        self.assertEqual(response.status_code, 200)

    def test_start_view_with_user_logged_in(self):
        self.client.login(username='john_doe', password='john_doe')
        response = self.client.post(reverse('Pymodoro:start'), {'tag': 'foo'})
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.u1.delete()
        self.u2.delete()