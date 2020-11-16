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
    last_time = models.DateTimeField()
    priority = models.BooleanField()
    learning = models.BooleanField()  # for reprioritisation
    sorted = models.BooleanField()
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


