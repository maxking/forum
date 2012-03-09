from django.forms.util import ErrorList
from django.contrib.auth.models import User
from django import forms 
from wiki.account.choices import *

class SignupForm(forms.Form):
    first_name=forms.CharField(max_length=25,label='First Name')
    last_name=forms.CharField(max_length=25,label='Last name')
    email=forms.EmailField()
    password1=forms.CharField(max_length=25, widget=forms.PasswordInput, label='Password')
    password2=forms.CharField(max_length=25, widget=forms.PasswordInput, label='Confirm Password')
    sex=forms.ChoiceField(choices=sex_choice)
    phno=forms.IntegerField(label='Phone Number')
    pin=forms.CharField(max_length=10)
    website=forms.URLField()
#    image=forms.FileField(label='Display Image', help_text='maximum 3MB' upload_to=)
    def clean(self):
        data=self.cleaned_data
        try:
            entered_email=data['email']
            password1=data['password1']
            password2=data['password2']
            user_qs=User.objects.all()
            for user in user_qs:
                if( entered_email==user.email ):
                    self._errors['email']=ErrorList(['Email already registerd please choose a different one'])
                if password1!=password2 :
                    self._errors['password2']=ErrorList(['Passwords do not match'])
                    del data['password1']
                    del data['password2']
                if username==user.username :
                    self._errors['username']=ErrorList(['Username already registered. Enter a different one.'])
                    del data['username']

        except:
            pass
        return data

class LoginForm(forms.Form):
    email=forms.EmailField(max_length=215)
    password=forms.CharField(max_length=125, widget=forms.PasswordInput, label='Password')
    
    def clean(self):
        data=self.cleaned_data
        try:
            email=data['email']
            user=User.objects.get( email = email )
        except Exception:
            self._errors['email'] = ErorList(['Not registered. Please register.'])
        return data


