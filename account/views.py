# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from wiki.root_views import get_base_vars
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.forms.util import ErrorList
import wiki.account.models as account_models
from wiki.account.forms import *
from django.core.files.base import ContentFile

def index(request):
    base_vars = get_base_vars(request)

    if request.user.is_authenticated(): #doesnt need to signup because already authenticated
        return HttpResponseRedirect("/account/home/")
    if request.method=="POST":
        # verify fields and login
        login_form=LoginForm( request.POST )
        if login_form.is_valid():
            email = request.POST['email']
            username = User.objects.get(email=email)
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                #authenticated so returning as authenticated
                login(request, user)
                return HttpResponseRedirect("/account/home")
            else:
                login_form._errors['email'] = ErrorList(['Wrong email or password'])
                base_vars.update({"login_form":login_form})
                return render_to_response("account_login.html", base_vars)
        else:
            base_vars.update({"login_form":login_form})
            return render_to_response("account_login.html", base_vars)
    else:
        base_vars.update({"login_form":LoginForm()})
        return render_to_response("account_login.html",base_vars)
    

def signupform(request):
    base_vars=get_base_vars(request)

    if request.user.is_authenticated():
        return HttpResponseRedirect("/account/home")
    else:
        base_vars.update({"reg_form":SignupForm()})
        return render_to_response("account_signup.html", base_vars)
            
def signup(request):
    base_vars=get_base_vars(request)
    
    if request.user.is_authenticated():
        base_vars.update({"message":"You are logged in."})
        return render_to_response("message.html", base_vars)
    else:
        if request.method=="POST":
            suForm=SignupForm(request.POST, request.FILES)
            if suForm.is_valid():
                pk=len(User.objects.all()).__str__()
                username=pk.join([request.POST['first_name'],request.POST['last_name']])
                user=User.objects.create_user( username=username,email=request.POST['email'],password=request.POST['password1'])
                user.first_name=request.POST['first_name']
                user.last_name=request.POST['last_name']
                user.save()
                
                person = account_models.person()
                person.user_id = user
                person.sex = request.POST['sex']
                person.phno = request.POST['phno']
                person.pin = request.POST['pin']
                person.website = request.POST['website']
                person.save()
                
                logged_in_user = authenticate(username=username, password=request.POST['password1'])
                if logged_in_user is not None:
                    login(request, logged_in_user)
                    return HttpResponseRedirect("/account/home")
            else:
                base_vars.update({"reg_form":suForm,})
                return render_to_response("account_signup.html", base_vars)
        else:
            base_vars.update({"reg_form":SignupForm()})
            return render_to_response("account_signup.html", base_vars)


def logout(request):
    if request.user.is_authenticated():
        auth_logout(request)
        return HttpResponseRedirect("/account/")
    else:
        base_vars=get_base_vars(request)

    base_vars.update({"message":"You are not authorised to be here"})
    return render_to_response("message.html",base_vars)

        
def home(request):
    base_vars = get_base_vars(request)
    
    if request.user.is_authenticated():
        email=base_vars['user']
        user = User.objects.get( email = email )
        _id = user.id
        person = account_models.person()
        person = account_models.person.objects.get( user_id = _id )
        base_vars.update({"email": email,"fname":user.first_name,"lname":user.last_name,"sex":person.sex, "phno":person.phno })
        return render_to_response("home.html",base_vars)
    else:
        HttpResponseRedirect("/account/")

def settings(request):
    base_vars = get_base_vars(request)
    
    try:
        pwdChng = request.GET['pwdChng']
        if(pwdChng == 'Sucess'):
            base_vars.update({'pwdMsg':"<span color=#008800>Password Changed</span><br>"})
        elif(pwdChng == 'Fail'):
            base_vars.update({'pwdMsg':"<span color=#008800>Password Change failed</span><br>"})
    
    except:
        pass

    if request.user.is_authenticated():
        user_current = User.objects.get(email=request.user.email)
        person_current = account_models.person.objects.get(user_id = user_current.pk)
        user_data = {}
        user_data['first_name'] = user_current.first_name
        user_data['last_name'] = user_current.last_name
        user_data['sex'] = person_current.sex
        user_data['phno'] = person_current.phno
        user_data['pin'] = person_current.pin
        user_data['website'] = person_current.website

        pool=AccountSettingsForm(user_data)
        base_vars.update({'pool': pool})
        return render_to_response("account_settings.html",base_vars)
    else:
        base_vars.update({"login_form":LoginForm()})
        return render_to_response("account_login.html",base_vars)

def change_password(request):
    if request.user.is_authenticated() and request.user.check_password( request.POST['old_pass'] ):
        user = request.user
        user.set_password( request.POST['new_pass'] )
        user.save()

    else:
        return HttpResponseRedirect('/account/settings?pwdChng=Fail')
    
    return HttpResponseRedirect('/account/settings?pwdChng=Sucess')

def change(request):
    if request.user.is_authenticated() and request.method == "POST":
        user = request.user
        person = account_models.person.objects.get(user_id = user)
        #assign values from form
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        
        person.sex = request.POST['sex']
        person.phno = request.POST['phno']
        person.website = request.POST['website']
        person.pin = request.POST['pin']
        person.save()

        return HttpResponseRedirect('/account/settings/')

    else:
        base_vars = get_base_vars(request)
        
        base_vars.update({"message":"You are not authorised to be here"})
        return render_to_response("message.html",message)
