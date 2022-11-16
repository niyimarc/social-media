from django.db import models
from profiles.models import Profile
from django.core.validators import FileExtensionValidator
# Create your models here.
# create a tuple to use in the CommentLike and PostLike model 
LIKE_CHOICES=(
    ('Like', 'Like'),
    ('Unlike', 'Unlike')
)


# create a model for Post 
class Post(models.Model):
    slug = models.SlugField(max_length=200, unique=True, blank = True, null = True)
    author = models.ForeignKey(Profile, on_delete = models.CASCADE, verbose_name= 'Author', related_name="posts")
    image = models.ImageField(upload_to='posts', blank = True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg' ])])
    liked = models.ManyToManyField(Profile, blank=True, related_name='post_likes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name = 'Post Contents')
    class Meta:
        ordering  = ['-created']
        
    def __str__(self):
        return str(self.content[:20])
    
    def num_likes(self):
        return self.liked.all().count()

    def num_comments(self): 
        # there is a reverse relationship in Comment model 
        # that is why I can use comment_set syntax 
        return self.comment_set.all().count() 

# create a model called PostLike like 
class PostLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    def __str__(self):
        return f"{self.user}-{self.post}-{self.value}"

# create a model for comment 
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    liked = models.ManyToManyField(Profile, blank=True, related_name='commentlikes')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)
    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


# create a model called comment like 
class CommentLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user}-{self.comment}-{self.value}"