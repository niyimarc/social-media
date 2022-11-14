from django.contrib import admin
from .models import Profile, Relationship
# Register your models here.

# register the Profile model 
admin.site.register(Profile)
# register the Relationship model 
admin.site.register(Relationship)
