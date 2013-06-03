from django.test import TestCase

from django.contrib.auth.models import User
from redeer.feeds.models import to_comma_separated, Group, Feed, Item


class SimpleTest(TestCase):
    def test_to_comma_separated(self):
        self.assertEqual(
            to_comma_separated([]), '')

        self.assertEqual(
            to_comma_separated([1]), '1')

        self.assertEqual(
            to_comma_separated([1, 2, 3]), '1,2,3')

    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class ManagerTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')
        Group.objects.create(user=self.user1)
        Group.objects.create(user=self.user2)
        Group.objects.create(user=self.user2)

    def test_counts(self):
        self.assertEqual(
            Group.objects.for_user(self.user1).count(),
            1
        )

        self.assertEqual(
            Group.objects.for_user(self.user2).count(),
            2
        )

    def test_id(self):
        self.assertEqual(
            Group.objects.for_user(self.user1.pk).count(),
            1
        )


class GroupTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.group = Group.objects.create(user=self.user, title='title')
        self.feed = Feed.objects.create(group=self.group)

    def test_unicode(self):
        self.assertEqual(
            unicode(Group.objects.get()),
            'title',
        )

    def test_to_dict(self):
        self.assertEqual(
            self.group.to_dict(),
            {
                'id': self.group.pk,
                'title': 'title',
            }
        )

    def test_feeds(self):
        self.assertEqual(
            self.group.feed_ids(),
            str(self.feed.pk)
        )

    def test_feedgroup(self):
        self.assertEqual(
            self.group.to_feedgroup_dict(),
            {
                'group_id': self.group.pk,
                'feed_ids': str(self.feed.pk),
            }
        )

    def test_mark_as_read(self):
        self.assertTrue(
            all(
                [not item.is_read for item in self.feed.item_set.all()]
            )
        )

        self.group.mark_read(is_read=True)

        self.assertTrue(
            all(
                [item.is_read for item in self.feed.item_set.all()]
            )
        )
