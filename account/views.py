from django.shortcuts import render
from .forms import CustomCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
import json

# Create your views here.


def validate_username(request):
    data = json.loads(request.body)
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': 'Username should contain only alphanumeric characters.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error':'Sorry username already in use, choose another.'}, status=409)   
    return JsonResponse({'username_valid': True}, status=200)


def signup(request):
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        fieldVals = request.POST
        username = request.POST['username']
        user_email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        context = {"fieldVals": fieldVals, 'form': form}
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already in use, choose another one.")
            return render(request, 'account/signup.html', context)
        if User.objects.filter(email=user_email).exists():
            messages.error(request, "sorry email already in use, please choose another one.")
            return render(request, 'account/signup.html', context)
        if len(password1) < 8:
            messages.error(request, "password must be 8 characters or more")
            return render(request, 'account/signup.html', context)
        if not (password1 == password2):
            messages.error(request, 'passwords did not match')
            return render(request, 'account/signup.html', context)            
        if form.is_valid():
            user = form.save()
            user.set_password(password1)
            user.is_active = False
            user.save()
            messages.success(request, mark_safe("Account created successfully.<br>Check your mail to activate account."))
    return render(request, 'account/signup.html', {'form': form})


def signin(request):
    return render(request, 'account/signin.html')