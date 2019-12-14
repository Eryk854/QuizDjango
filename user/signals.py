from django.db.models.signals import post_save
from .models import Account, Player
from django.dispatch import receiver


@receiver(post_save, sender=Player)
def create_player(sender, instance, created, **kwargs):
    print('bbbb')
    if created:
        print('aaaa')
        Player.objects.create(email=instance)


@receiver(post_save, sender=Player)
def save_player(sender, instance, **kwargs):
    print('cccc')
    instance.profile.save()
