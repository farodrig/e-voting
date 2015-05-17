# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.db.models import Q
from forms import UserForm, PollForm, QuestionForm, AnswerForm
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
        if poll_form.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = request.user
            poll.save()
            return redirect('/createquestion/'+str(poll.id))
    poll_form = PollForm()
    return render_to_response("create_poll.html", {'poll_form': poll_form}, context_instance=RequestContext(request))


def createQuestion(request, poll_id):
    if (poll_id == None):
        return redirect("/")
    if request.method == "POST":
		question_form = QuestionForm(data=request.POST)
		cforms = [AnswerForm(request.POST, prefix=str(x), instance=Answer()) for x in range(1,3)]
		if question_form.is_valid(): #falta validar por la respuesta.
			question = question_form.save(commit=False)
			question.poll = Poll.objects.get(id=poll_id)
			type = Type.objects.get(id=1)
			question.type = type
			question.save()
			for cf in cforms:
				answer = cf.save(commit=False)
				answer.question = question
				answer.save()
			if request.POST['continuar'] == "1":
				return render_to_response("create_question.html", context_instance=RequestContext(request))
			else:
				return redirect('/invitation_list/'+poll_id)
    return render_to_response("create_question.html", {'poll':Poll.objects.get(id = poll_id)}, context_instance=RequestContext(request))


def search(request):
	try:
        #Deberia tambien filtrar que no se haya respondido antes o no??
		polls = Poll.objects.filter(Q(privacy_status="P"), ~Q(creator = request.user))
	except:
		polls = None
	return render_to_response("poll_public.html", {"polls":polls}, context_instance=RequestContext(request))


def answer(request, idpoll):
    if (idpoll==None):
        return redirect("/")
    poll = Poll.objects.get(pk=idpoll)
    if request.method == "POST":
        answers =  request.POST.getlist('ans')
        for ans in answers:
            vote = Vote(answer = Answer.objects.get(id = ans), voter = request.user)
            vote.save()
        invitation = Invitation.objects.get(poll = poll, guest = request.user)
        invitation.answered = True
        invitation.save()
        return redirect("/")
    dict={}
    dict['poll']=poll
    questList=[]
    questions=Question.objects.filter(poll=poll)
    for ques in questions:
        q={}
        answers=Answer.objects.filter(question=ques)
        ansList=[]
        for ans in answers:
            ansList.append({'text':ans.text, 'id':ans.id})
        q['id'] = ques.id
        q['name']=ques.name
        q['answers']=ansList
        questList.append(q)
    dict['questions']=questList
    return render_to_response("poll_answer.html", dict, context_instance=RequestContext(request))


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


def invitation_list(request, poll_id):
    if(poll_id==None):
        return redirect("/")
    if request.method == 'POST':
        guests=request.POST.getlist('guests[]')
        for guest in guests:
            invitation = Invitation(poll=Poll.objects.get(id=poll_id),guest=User.objects.get(id = int(guest)))
            invitation.save()
        return redirect('/')
    guests = [request.user.id]
    for invitation in Invitation.objects.filter(poll = poll_id):
        guests.append(invitation.guest.id)
    users=User.objects.all().exclude(id__in=guests)
    return  render_to_response('invitation_list.html', {'users': users, 'poll':poll_id}, context_instance=RequestContext(request))


def results(request, poll_id):
    if(poll_id==None):
        return redirect("/")
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
            try:
                a['perc']=100.0*votes/total
            except:
                a['perc'] = 0.0
            ansList.append(a)
        q['name']=name
        q['answers']=ansList
        questList.append(q)
    dict['questions']=questList
    return  render_to_response('poll_results.html', dict, context_instance=RequestContext(request))


def all(items):
    import operator
    return reduce(operator.and_, [bool(item) for item in items])
