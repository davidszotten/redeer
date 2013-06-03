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
        self.group1 = Group.objects.create(user=self.user, title='title')
        self.group2 = Group.objects.create(user=self.user, title='title')
        self.feed1 = Feed.objects.create(group=self.group1)
        self.feed2 = Feed.objects.create(group=self.group2)
        self.item1 = Item.objects.create(feed=self.feed1, created_on_time=0)
        self.item2 = Item.objects.create(feed=self.feed2, created_on_time=0)

    def test_unicode(self):
        self.assertEqual(
            unicode(self.group1),
            'title',
        )

    def test_to_dict(self):
        self.assertEqual(
            self.group1.to_dict(),
            {
                'id': self.group1.pk,
                'title': 'title',
            }
        )

    def test_feeds(self):
        self.assertEqual(
            self.group1.feed_ids(),
            str(self.feed1.pk)
        )

    def test_feedgroup(self):
        self.assertEqual(
            self.group1.to_feedgroup_dict(),
            {
                'group_id': self.group1.pk,
                'feed_ids': str(self.feed1.pk),
            }
        )

    def test_mark_as_read(self):
        self.assertFalse(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)

        self.group1.mark_read(is_read=True)

        self.assertTrue(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)


class FeedTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.group1 = Group.objects.create(user=self.user, title='title')
        self.group2 = Group.objects.create(user=self.user, title='title')
        self.feed1 = Feed.objects.create(group=self.group1)
        self.feed2 = Feed.objects.create(group=self.group2)
        self.item1 = Item.objects.create(feed=self.feed1, created_on_time=0)
        self.item2 = Item.objects.create(feed=self.feed2, created_on_time=0)

    def test_mark_as_read(self):
        self.assertFalse(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)

        self.feed1.mark_read(is_read=True)

        self.assertTrue(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)


class ItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user')
        self.group1 = Group.objects.create(user=self.user, title='title')
        self.group2 = Group.objects.create(user=self.user, title='title')
        self.feed1 = Feed.objects.create(group=self.group1)
        self.feed2 = Feed.objects.create(group=self.group2)
        self.item1 = Item.objects.create(feed=self.feed1, created_on_time=0)
        self.item2 = Item.objects.create(feed=self.feed2, created_on_time=0)

    def test_mark_as_read(self):
        self.assertFalse(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)

        self.item1.mark_read(is_read=True)

        self.assertTrue(Item.objects.get(pk=self.item1.pk).is_read)
        self.assertFalse(Item.objects.get(pk=self.item2.pk).is_read)
