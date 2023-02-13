from django.shortcuts import render, redirect, reverse
from .forms import CustomCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.utils.safestring import mark_safe
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from . utils import token_generator
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import json

# Create your views here.


def validate_username(request):
    data = json.loads(request.body)
    username = data['username']
    if not str(username).isalnum():
        return JsonResponse({'username_error': 'Username should contain only alphanumeric characters.'}, status=400)
    if User.objects.filter(username=username).exists():
        return JsonResponse({'username_error': 'Sorry username already in use, choose another.'}, status=409)   
    return JsonResponse({'username_valid': True}, status=200)


def validate_email(request):
    data = json.loads(request.body)
    email = data['email']
    if User.objects.filter(email=email):
        return JsonResponse({'email_error': 'Sorry, email already taken.'}, status=409)
    try:
        validate_email(email)
        return JsonResponse({'email_valid': True}, status=200)
    except ValidationError:
        return JsonResponse({'email_error': 'Invalid email'}, status=400)


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
            # call emailactivation here
            # activate_email(request, user, user_email)
            email_subject = 'Activate your account'
            # body of email should contain the followings
            # -path to view
            # -get domain we are in
            # -get relative url
                
            # -get token
            # token = token_generator.make_token(user)
            # - encode uid
            # uid64 = urlsafe_base64_encode(force_bytes(user.pk))
            # -get domain we are in
            # domain = get_current_site(request).domain
            # -get relative url
            # link = reverse('account:activate', kwargs={'uid64': uid64,'token': token_generator.make_token(user)})
            # activate_link = 'http://'+domain+link
            email_body = 'Hello '+user.username+', please use the link below to verify your account\n'#+activate_link
            email = EmailMessage(email_subject, email_body, 'noreply@mrdee.com', [user_email] )
            # email.send(fail_silently=True)
            messages.success(request, mark_safe("Account created successfully.<br>Check your mail to activate account."))
            return render(request, 'account/signup.html')           
            # return redirect('account:signup')
            # messages.success(request, mark_safe("Account created successfully.<br>Check your mail to activate account."))
    return render(request, 'account/signup.html', {'form': form})


# def activate_email(request, user, to_email):
#     mail_subject = 'Activate your user account'
#     uid = urlsafe_base64_encode(force_bytes(user.pk))
#     link = reverse('account:activate', kwargs={'uid64':uid,'token':token_generator.make_token(user)})
#     message = render_to_string('account/template_activate_account.html', {
#         'user': user.username,
#         'domain': get_current_site(request).domain,
#         # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'link': link,
#         'token': token_generator.make_token(user),
#         'protocol': 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
#             received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
#     else:
#         messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uid64, token):
    User = get_user_model()
    try:
        id = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(pk=id)
        if not token_generator.check_token(user, token):
            messages.warning(request, 'user alredy activated')
            return redirect('account:login')
        if user.is_active:
            return redirect('account:login')
        user.is_active = True
        user.save()
        messages.success(request,'Account successfully activated')
        return redirect('account:login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return redirect('account:login')


def signin(request):
    return render(request, 'account/signin.html')