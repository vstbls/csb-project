from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Message
import sqlite3

def loginView(request):
    return render(request, 'pages/login.html')

def processLoginView(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username')).first()
        if user is None:
            return HttpResponse('User does not exist.')
        if user.password == request.POST.get('password'):
            request.session['username'] = user.username
            return redirect(f'/chat/{user.username}/')
            # This leads to broken access control! A user can view the messages of other users just by changing the URL!
            # This can be fixed by.... doing something...
        else:
            return redirect('/')

def chatView(request, username):
    user = User.objects.get(username=username)
    received = Message.objects.filter(receiver=user)
    recipients = User.objects.exclude(username=username)
    sent = Message.objects.filter(sender=user)
    return render(request, 'pages/chat.html', {'username': username, 'received': received, 'sent': sent, 'recipients': recipients})

def sendMessageView(request):
    to = request.GET.get('to')
    to_user = User.objects.get(username=to)
    from_user = User.objects.get(username=request.session['username'])
    content = request.GET.get('content')
    Message.objects.create(sender=from_user, receiver=to_user, content=content)
    return redirect(f'/chat/{request.session["username"]}/')

def searchView(request):
    searchstring = request.POST.get('searchstring', '').strip()
    uid = User.objects.get(username=request.session['username']).id
    filtered = Message.objects.raw("SELECT * FROM pages_message WHERE receiver_id=" + str(uid) + " and content LIKE '%" + searchstring + "%'")
    #conn = sqlite3.connect('../db.sqlite3')
    #c = conn.cursor()
    #filtered = c.execute("SELECT content FROM pages_message WHERE receiver_id=" + str(uid) + "and content LIKE '%" + searchstring + "%'").fetchall()
    return render(request, 'pages/search.html', {'searchstring': searchstring, 'messages': filtered})