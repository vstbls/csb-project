from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Message

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def loginView(request):
    return render(request, 'pages/login.html')

def processLoginView(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username')).first()
        if user is None:
            return HttpResponse('User does not exist.')
        if user.password == request.POST.get('password'):
            return redirect(f'/chat/{user.username}/')
            # This leads to broken access control! A user can view the messages of other users just by changing the URL!
            # This can be fixed by.... doing something...
        else:
            return redirect('/')

def chatView(request, username):
    return render(request, 'pages/chat.html', {'username': username})