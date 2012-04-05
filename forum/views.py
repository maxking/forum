# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from wiki.root_views import get_base_vars
from wiki.forum.views import *
from wiki.forum.models import post as post_model
from wiki.forum.forms import PostForm
import datetime
from django.contrib.auth.models import User

def newpost(request):
    base_vars = get_base_vars(request)
    
    if request.user.is_authenticated():
        email = base_vars['user']
        user = User.objects.get( email = email )
        user_name = "%s %s" %(user.first_name,  user.last_name)
        if request.method=="POST":
            new_post = PostForm(request.POST)
            if new_post.is_valid():
                post = post_model()
                post.posted_by = user_name
                post.title = request.POST['title']
                post.message = request.POST['message']
                post.date = datetime.datetime.now()
                post.save()
                
                return HttpResponseRedirect('/forum/')
            
            else:
                base_vars.update({"post_form":PostForm})
                return render_to_response("new_post.html",base_vars)
        
        else:
            base_vars.update({"post_form":PostForm})
            return render_to_response("new_post.html",base_vars)
    else:
        base_vars.update({"message":"Please login to view this page"})
        return render_to_response("message.html", base_vars)
        
