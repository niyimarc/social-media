from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship

# the Profile receiver 
@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# the Relationship receiver 
@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    receiver_ = instance.receiver
    # execute the code if the status is 'accepted' 
    if instance.status =='accepted':
        # define the friend request sender 
        sender_.friends.add(receiver_.user)
        # define the friend request receiver 
        receiver_.friends.add(sender_.user)
        sender_.save()
        receiver_.save()