from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Message

def loginView(request):
    return render(request, 'pages/login.html')

def processLoginView(request):
    if request.method == 'POST':
        user = User.objects.filter(username=request.POST.get('username')).first()
        if user is None:
            return HttpResponse('User does not exist.')
        '''
        FIX FOR SENSITIVE DATA EXPOSURE:
        We first need to protect the presently stored passwords by hashing them,
        for example by iterating over all of them:
        
        for u in User.objects.all():
            u.password = make_password(u.password)
            u.save()
        
        This migration only needs to be performed once by server admins. After that,
        it's enough to change the following if-statement to:
        
        if checkpassword(user.password, request.POST.get('password')):
        '''
        if user.password == request.POST.get('password'):
            request.session['username'] = user.username
            # Fix for broken access control: Change redirect to redirect('/chat/'). Details below.
            return redirect(f'/chat/{user.username}/')
        else:
            return redirect('/')
'''
FIX FOR BROKEN ACCESS CONTROL:
For this, we want to remove the possibility of viewing messages by changing the URL.
Since the app already stores the signed in user's username in request.session on login,
we can use that instead:

def chatView(request):
    username = request.session['username']
    user = User.objects.get(username=username)
    received = Message.objects.filter(receiver=user)
    recipients = User.objects.exclude(username=username)
    sent = Message.objects.filter(sender=user)
    return render(request, 'pages/chat.html', {'username': username, 'received': received, 'sent': sent, 'recipients': recipients})
    
We also need to change URL handling in urls.py
'''
def chatView(request, username):
    user = User.objects.get(username=username)
    received = Message.objects.filter(receiver=user)
    recipients = User.objects.exclude(username=username)
    sent = Message.objects.filter(sender=user)
    return render(request, 'pages/chat.html', {'username': username, 'received': received, 'sent': sent, 'recipients': recipients})

def sendMessageView(request):
    '''
    FIX FOR CSRF: Use POST requests instead of GET:
    
    to = request.POST.get('to')
    [...]
    content = request.POST.get('content')
    
    This way messages will no longer be able to be sent using URLs.
    '''
    to = request.GET.get('to')
    to_user = User.objects.get(username=to)
    from_user = User.objects.get(username=request.session['username'])
    content = request.GET.get('content')
    Message.objects.create(sender=from_user, receiver=to_user, content=content)
    # Fix for broken access control: Change redirect to redirect('/chat/'). Details above.
    return redirect(f'/chat/{request.session["username"]}/')

def searchView(request):
    searchstring = request.POST.get('searchstring', '').strip()
    uid = User.objects.get(username=request.session['username']).id
    '''
    FIX FOR SQL INJECTION:
    The issue is relying on string formatting for constructing the query.
    The query can be constructed safely without string formatting using Django's raw():
    
    filtered = Message.objects.raw(
        "SELECT * FROM pages_message WHERE receiver_id=%s and content LIKE '%%s%'",
        [str(uid), searchstring]
        )
    '''
    filtered = Message.objects.raw("SELECT * FROM pages_message WHERE receiver_id=" + str(uid) + " and content LIKE '%" + searchstring + "%'")
    return render(request, 'pages/search.html', {'searchstring': searchstring, 'messages': filtered})