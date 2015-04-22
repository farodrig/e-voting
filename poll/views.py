from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

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