from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from authentication.forms import RegisterForm, LoginForm


class RegisterView(View):
    @staticmethod
    def get(request):
        return render(request, 'register.html', {"form": RegisterForm()})

    @staticmethod
    def post(request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return redirect('index')
        return render(request, 'register.html', {"form": form})


class LoginView(View):
    @staticmethod
    def get(request):
        return render(request, 'login.html', {"form": LoginForm()})

    @staticmethod
    def post(request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            return redirect('index')
        return render(request, 'login.html', {"form": form})
