from django.test import TestCase
from .models import(
    User,
    UserCard,
    Card,
    UserDeck,
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


class UserDeckTests(TestCase):

    def test_create(self):
        u = User()
        c = Card()
        u.save()
        c.save()
        uc = UserCard(
            user=u, card=c
        )
        uc.save()
        ud = UserDeck(user=u)
        ud.save()
        ud.cards.add(uc)
        self.assertEqual(len(ud.cards.all()), 1)
        self.assertEqual(ud.card_total, 1)

    def test_organise_cards(self):
        u = User()
        c = Card()
        u.save()
        c.save()
        uc = UserCard(
            user=u, card=c
        )
        uc.save()
        ud = UserDeck(user=u)
        ud.save()
        ud.cards.add(uc)
        ud.organise_cards()
        self.assertEqual(len(ud.seen_cards), 0)
        self.assertEqual(len(ud.unseen_cards), 1)
        self.assertEqual(len(ud.learning_cards), 0)
