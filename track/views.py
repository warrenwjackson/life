import datetime
import traceback

from django.core.context_processors import csrf
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required



import modelutils

def loginview(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)

def sign_up_in(request):
    post = request.POST
    if not modelutils.user_exists(post['email']): 
        user = modelutils.create_user(username=post['email'], email=post['email'], password=post['password'])
    return auth_and_login(username=post['email'], password=post['password'], request=request, next='/')
        
def auth_and_login(username, password, request, next='/'):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/login')    

@login_required(login_url='/login/')
def entry(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('entry.html', c)

@login_required(login_url='/login/')
def day(request):
    user = request.user
    if request.method == 'POST':
        post = request.POST
#        day = post.get('date')  #TODO: once I figure out a mobile friendly datepicker in JQuery Mobile. 
        day = datetime.date.today()
        modelutils.record_day(user, day, happiness=post.get('happiness'), work=post.get('work'), case=post.get('case'), content=post.get('content'))
        return redirect('/summary/')
#        return redirect('/summary/')

@login_required(login_url='/login/')
def summary(request):
    history = modelutils.user_history(request.user)
    happiness_work = [list(x) for x in zip(history['work'],history['happiness'])]
    return render_to_response('display.html', locals())
