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
        if poll_form.is_valid():
            poll = poll_form.save()
            poll.creator = request.user
            poll.save()
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

#TO DO Cate
#Puedes ver lo q esta mostrando ahora en localhost:8000/invitation_list por ahora, es estatico
#Te recuerdo q en django, el modelo se llama modelo, la vista se llama template y el controlador se llama vista.
#En urls.py hay un dispatcher, q toma una expresion regular y le asigna un controlador para q responda a el llamado de la URL.

def invitation_list(request):
    if request.method == 'POST':
        guests=request.POST.getlist('guests')
        for guest in guests:
            invitation = Invitation()
            invitation.set_poll(1)
            invitation.set_guest(guest)
            invitation.save()
            return redirect('/')
    else:
        users=User.objects
    #poll = 1 #Deberia sacarse de la sesion, dejemosla harcodeada por ahora. Tiene q estar creada alguna poll con id 1 para q esto funcione xD
    #verificar si metodo es post
    #si es post, sacar datos de invitados con 'some_var = request.POST.getlist('guests')' somevar arreglo de id de usuarios que seran invitados. Guardar estos invitados en la tabla de invitaciones. Redirigir a alguna pagina.
    #si no es post, buscar a todos los usuarios y crear variable con ellos, abajo esta nombrada como users
    #users = 1 #Por poner algo, users deberian ser todos los usuarios q sacaste de la bse de datos
    #render to response recibe primero el template, luego un diccionario de {'nombre_variable_en_template': nombre_variable_controlador, ...mas asocioaciones...} y la otra cosa, es mejor q siempre este xD.
    return  render_to_response('invitation_list.html', {'users': users}, context_instance=RequestContext(request))