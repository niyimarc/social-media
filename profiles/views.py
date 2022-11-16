from django.shortcuts import render
from .models import Profile
from .forms import NameModelForm, AvatarModelForm, BioModelForm
from django.http import HttpResponseRedirect

# Create your views here.

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    nameform = NameModelForm(request.POST, instance=profile)
    bioform = BioModelForm(request.POST, instance=profile)
    avatarform = AvatarModelForm(request.POST or None, request.FILES or None, instance=profile)
    # I will set the initial value of confirm to False 
    # whenever I successfully submit a form, I wan the confirm value back to false 
    # I will add it to the contex so I can use in the template
    confirm = False

    # form me to be able to use multiple forms in a view,
    # I have to use the attribute name="" in the submit button. 

    # if method="POST" and name="btnname" submit this form
    if request.method == 'POST' and 'btnname' in request.POST:
        if nameform.is_valid():
            nameform.save(commit=True)
            # change the value of confirm to True 
            confirm = True

    # if method="POST" and name="btnbio" submit this form
    if request.method == 'POST' and 'btnbio' in request.POST:
        if bioform.is_valid():
            bioform.save(commit=True)
            # change the value of confirm to True 
            confirm = True

    # if method="POST" and name="btnavatar" submit this form
    if request.method == 'POST' and 'btnavatar' in request.POST:
        if avatarform.is_valid():
            avatarform.save(commit=True)
            # change the value of confirm to True 
            confirm = True
            

    contex = {
        'profile': profile,
        'nameform': nameform,
        'avatarform': avatarform,
        'bioform': bioform,
        'confirm': confirm,
    }
    return render(request, 'profiles/myprofile.html', contex)