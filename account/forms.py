from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from . models import Profile


class CustomCreationForm(UserCreationForm):
    # username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'text','placeholder':'Username','name':'username','id':'usernameField','value':""}))
    # # first_name = forms.CharField(max_length=100, label="", widget=forms.TextInput(attrs={'class':'text','placeholder':'Firstname','name':'firstname','id':'firstnameField','value':""}))
    # # last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'text','placeholder':'Lastname','name':'lastname','id':'lastnameField','value':""}))
    # email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'text email','placeholder':'Email','name':'email','id':'emailField','value':""}))
    # password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'text','placeholder':'Password','name':'password1','id':'password1Field'}))
    # password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'text w3lpass','name':'password2','id':'password2Field','placeholder':'Confirm Password'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


genders = (('male', 'male'), ('female', 'female'),)


class ProfileUpdateForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=genders, widget=forms.RadioSelect(attrs={'placeholder':'gender'}))
    bio = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Enter bio ...'}))
    phone = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Telephone'}))
    country = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country'}))
    city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'city'}))
    occupation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'occupation'}))
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address'}))
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'company'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control','placeholder':'Upload your avatar'}))

    class Meta:
        model = Profile
        fields = ['gender','bio','phone','country','city','occupation','address','company','avatar']