from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UserForm,LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.template import RequestContext

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('board:post_list')
        else:
            return HttpResponseRedirect('/error/')
    else:
        form = UserForm()
        return render(request,'Account/adduser.html',{'form':form})
# Create your views here.
def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect('board:post_list')
        else:
            return HttpResponseRedirect('/esignin/')
    else:
        form = LoginForm()
        return render(request,'Account/login.html',{'form':form})
def esignin(request):
    return render(request,'Account/esignin.html')
def error(request):
    return render(request,'Account/error.html')
