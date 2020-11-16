from django.test import TestCase
from .models import(
    User,
    UserCard,
    Card,
)


class UserCardTests(TestCase):

    def test_create(self):
        u = User()
        c = Card()
        uc = UserCard(
            user=u, card=c
        )
        self.assertEqual(uc.user, u)
        self.assertEqual(uc.card, c)

    def test_create_two(self):
        u = User()
        c = Card()
        uc = UserCard(
            user=u, card=c
        )
        uc2 = UserCard(
            user=u, card=c
        )
        self.assertEqual(uc.user, u)
        self.assertEqual(uc.card, c)
        self.assertEqual(uc2.user, u)
        self.assertEqual(uc2.card, c)
