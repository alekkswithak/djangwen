import math
from collections import defaultdict
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Card(models.Model):
    name = models.CharField(max_length=64)
    frequency = models.IntegerField(default=0)


class UserCard(models.Model):
    ease = models.IntegerField(default=1)
    last_time = models.DateTimeField(null=True)
    priority = models.BooleanField(default=False)
    learning = models.BooleanField(default=False)  # for reprioritisation
    sorted = models.BooleanField(default=False)
    to_study = models.BooleanField(default=True)

    card = models.OneToOneField(Card, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def known(self, multiplier):
        self.ease *= multiplier
        if self.priority is True:
            self.priority = False
        else:
            self.learning = False
        self.last_time = datetime.now()

    def unknown(self, multiplier):
        ease = self.ease / multiplier
        if ease > 1:
            self.ease = math.floor(ease)
        else:
            self.ease = 1
        self.priority = True
        self.last_time = datetime.now()

    def get_questions(self):
        return self.card.get_questions()

    def get_answers(self):
        return self.card.get_answers()


class UserDeck(models.Model):
    name = models.CharField(max_length=64)
    card_number = models.IntegerField(default=20)
    new_card_number = models.IntegerField(default=10)
    card_counter = models.IntegerField(default=0)
    multiplier = models.IntegerField(default=2)
    entry_interval = models.IntegerField(default=5)
    last_date = models.DateField(null=True)

    cards = models.ManyToManyField(UserCard)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def card_total(self):
        return len(self.cards.all())

    def populate(self, deck):
        self.deck = deck
        self.name = deck.name
        for c in deck.cards:
            uc = UserCard(card=c)
            uc.save()
            self.cards.add(uc)

    def organise_cards(self):
        self.seen_cards = self.cards.filter(last_time__isnull=False).all()
        self.unseen_cards = self.cards.filter(last_time__isnull=True).all()
        self.learning_cards = self.cards.filter(learning=True).all()

    def shuffle(self):
        self.organise_cards()
        if len(self.seen_cards) == 0:
            card_number = min(self.card_number, self.card_total)
            for c in self.unseen_cards[0:card_number]:
                c.learning = True
            return

        min_time = min(self.seen_cards, key=lambda c: c.last_time).last_time
        delta_cards = defaultdict(list)
        for c in self.seen_cards:
            if c.to_study:
                delta = (c.last_time - min_time).total_seconds()
                delta_cards[delta*c.ease].append(c)
                if not c.priority:
                    c.learning = False

        counter = 0
        while counter < self.card_number:
            for c in delta_cards[min(delta_cards)]:
                c.learning = True
                counter += 1
            del delta_cards[min(delta_cards)]
            if len(delta_cards) == 0:
                break

        counter = 0
        for c in self.unseen_cards:
            if c.to_study:
                c.learning = True
                counter += 1
                if counter == self.new_card_number:
                    break

    def get_learning_cards(self):
        if len([c for c in self.cards if c.learning]) == 0:
            self.shuffle()
        return [c for c in self.cards if c.learning]

    def play_outcomes(self, outcomes):
        """
        plays as many cards as there are in outcomes
        outcomes :
        {
            '1': {'id': '2516', 'result': 'x'},
            '2': {'id': '2517', 'result': 'z'},
            'deck_id': '6' # not here?
        }

        """
        for i in range(0, len(outcomes) - 1):
            outcome_row = outcomes[str(i+1)]
            card_id = int(outcome_row.get('id'))
            card = UserCard.query.get(card_id)
            result = outcome_row.get('result')
            if result == 'z':
                card.known(self.multiplier)
            elif result == 'x':
                card.unknown(self.multiplier)

    def process_sort(self, outcomes):
        for i in range(0, len(outcomes) - 1):
            outcome_row = outcomes[str(i+1)]
            card_id = int(outcome_row.get('id'))
            card = UserCard.query.get(card_id)
            result = outcome_row.get('result')
            if result == 'z':
                card.to_study = False
            elif result == 'x':
                card.to_study = True
            card.sorted = True

    def get_unsorted_cards(self):
        return [c for c in self.cards if not c.sorted]

    def get_flash_cards(self, sorting=False):
        flash_cards = []
        if sorting is False:
            deck_cards = self.get_learning_cards()
        else:
            deck_cards = self.get_unsorted_cards()
        i = 0
        for c in deck_cards:
            tc = c.get_dict()
            tc['i'] = i
            tc['ease'] = c.ease
            i += 1
            flash_cards.append(tc)

        return flash_cards

    def get_display_cards(self):
        cards = defaultdict(list)
        for c in self.cards.all():
            if c.to_study:
                cards[1].append(c)
            else:
                cards[2].append(c)
        return cards

    def seen_total(self):
        to_study = [c for c in self.cards if c.to_study]
        return len([c for c in to_study if c.last_time])

    def to_study_total(self):
        return len([c for c in self.cards if c.to_study])

