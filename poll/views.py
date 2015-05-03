from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from forms import UserForm, PollForm
from django.http import HttpResponse
from models import *
import datetime
# Create your views here.

def main(request):
     return render_to_response("main.html", context_instance=RequestContext(request))

def validate(request):
    form = AuthenticationForm(request)
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        user = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=user, password=password)
        if user is not None and form.is_valid():
            if user.is_active:
                login(request, user)
                return redirect('/')
    content =  {'form': form}
    return render_to_response("signin.html", content, context_instance=RequestContext(request))

def out(request):
    logout(request)
    return redirect('/')

def createPoll(request):
	if request.method == "POST":
		#falta validar el id del user
		poll_form = PollForm(data={'name':request.POST['name'], 'init_date':request.POST['init_date'], 'close_date':request.POST['close_date'], \
		'privacy_status':request.POST['privacy_status'], 'creator' : request.POST['creator']})
		if poll_form.is_valid():
			poll = poll_form.save()
			return redirect('/')
	else:
		poll_form = PollForm()
	return render_to_response("create_poll.html", {'poll_form': poll_form}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)
            return redirect('/')

    else:
        user_form = UserForm()
    return render_to_response('signup.html', {'user_form': user_form}, context_instance=RequestContext(request))

def poll_list(request):
    try:
        created = Poll.objects.filter(creator = request.user)
    except:
        created = None
    try:
        answered = Invitation.objects.filter(guest = request.user, answered = True)
    except:
        answered = None
    try:
        not_answered = Invitation.objects.filter(guest = request.user, answered = False)
    except:
        not_answered = None
    return render_to_response('poll_list.html', {'created': created, 'answered': answered, 'not_answered': not_answered, 'now': datetime.datetime.now()},context_instance=RequestContext(request))