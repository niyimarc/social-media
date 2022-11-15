from django.db import models
from django.contrib.auth.models import User
from .utils import get_random_code
from django.template.defaultfilters import slugify
# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='No bio...', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    address = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # define a method to get all friends
    def get_friends(self):
        return self.friends.all()

    # define a method to get the total number of friends 
    def get_friends_no(self):
        return self.friends.all().count()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
    
    # create slug from first_name and last_name or from user
    def save(self, *args, **kwargs):
        ex = False
        if self.first_name and self.last_name:
            # create the slug with first_name and last_name if 
            # there is no user with the same first_name and last_name
            to_slug = slugify(str(self.first_name) + " " + str(self.last_name))
            # check if to_slug does not exist 
            ex = Profile.objects.filter(slug=to_slug).exists()

            # create the slug with first_name, last_name and get_random_code if 
            # there is user with the same first_name and last_name 
            while ex:
                to_slug = slugify(to_slug + " " + str(get_random_code()))
                ex = Profile.objects.filter(slug=to_slug).exists()
        else:
            to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_CHOICES=(
    ('send', 'send'),
    ('accepted', 'accepted')
)
class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"


    


