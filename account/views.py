from django.shortcuts import render
from .forms import CustomCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.utils.safestring import mark_safe
from django.contrib import messages

# Create your views here.


def signup(request):
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        password1 = request.POST.get('password1')
        if form.is_valid():
            user = form.save()
            user.set_password(password1)
            user.is_active = False
            user.save()
            messages.success(request, mark_safe("Account created successfully.<br>Check your mail to activate account."))
    return render(request, 'account/signup.html', {'form': form})