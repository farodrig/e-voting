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
        poll_form = PollForm(data=request.POST)
        print poll_form
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = request.user
            print poll
            poll.save()
            return render_to_response("create_question.html", {'poll': poll}, context_instance=RequestContext(request))
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


def invitation_list(request):
    if request.method == 'POST':
        guests=request.POST.getlist('guests[]')
        print guests
        for guest in guests:
            invitation = Invitation(poll=Poll.objects.get(id=1),guest=User.objects.get(id = int(guest)))
            invitation.save()
        return redirect('/')
    else:
        users=User.objects.all()
    return  render_to_response('invitation_list.html', {'users': users}, context_instance=RequestContext(request))

#TO DO CATE
#Recuerda crear preguntas, respuestas y votos para q veas q va funcionando
def results(request):
    poll_id = 1 #harcodeado no mas
    dict={}
    poll=Poll.objects.get(id=poll_id)
    dict['poll']=poll
    questList=[]
    questions=Question.objects.filter(poll=poll)
    for ques in questions:
        q={}
        name=ques.name
        answers=Answer.objects.filter(question=ques)
        total=Vote.objects.filter(answer__in=answers).count()
        ansList=[]
        for ans in answers:
            a={}
            text=ans.text
            votes=Vote.objects.filter(answer=ans).count()
            a['text']=text
            a['votes'] = votes
            a['perc']=100.0*votes/total
            ansList.append(a)
        q['name']=name
        q['answers']=ansList
        questList.append(q)
    dict['questions']=questList
    return  render_to_response('poll_results.html', dict, context_instance=RequestContext(request))
