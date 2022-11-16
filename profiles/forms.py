from django import forms
from .models import Profile

class NameModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name',)


class AvatarModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar',)

class BioModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio',)