from django.http import HttpResponse
from django.shortcuts import render

def home_view(request):
    user = request.user
    hello = 'Hello world'
    contex = {
        'user': user,
        'hello': hello
    }
    # return HttpResponse('Hello world')
    return render(request, 'main/home.html', contex )