from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def notAUser(response):
    return render(response,'notAUser.html')

def home(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    else:
        form = RegisterForm()
        return render(response, "signup.html", {"form":form})

def accountpage(request):
    if request.user.is_authenticated:
        return render(request, 'account.html')
    else:
        return redirect("http://127.0.0.1:8000/account/login/")

def delete(response):
    return render(response,'delete.html')

def delete_account(request):
    u = User.objects.get(username=request.user.username)
    u.delete()

