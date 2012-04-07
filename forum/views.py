# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from wiki.root_views import get_base_vars
from wiki.forum.views import *
from wiki.forum.models import post as post_model
from wiki.forum.models import comment as comment_model
from wiki.forum.forms import PostForm, CommentForm
import datetime
from django.contrib.auth.models import User

def newpost(request):
    base_vars = get_base_vars(request)
    
    if request.user.is_authenticated():
        email = base_vars['user']
        user_name = base_vars['user_name']
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
        

def forum_index(request):
    base_vars = get_base_vars(request)
    count_comment = {}
    if request.user.is_authenticated():
        posts = post_model.objects.all()

        for post in posts:
            comments = comment_model.objects.filter( parent_post_id = post.id ).count()
            count_comment[ post.id ] = comments

        base_vars.update({"posts" : posts ,"count": count_comment})
        return render_to_response('forum.html',base_vars)
    
    else:
        base_vars.update({"message":"You are not authorised to be here"})
        return render_to_response("message.html", base_vars)


def post_page(request,post_id):
    base_vars = get_base_vars(request)
    
    if request.user.is_authenticated():
        email = base_vars['user']
        user = User.objects.get( email = email )
        user_name = "%s %s" %(user.first_name , user.last_name )
        post = post_model.objects.get( id=post_id )
        comment_post = comment_model.objects.filter( parent_post_id = post_id ).order_by( 'date' )
        if request.method == "POST":
            new_comment = CommentForm(request.POST)
            if new_comment.is_valid():
                comment = comment_model()
                comment.posted_by = user_name
                comment.date = datetime.datetime.now()
                comment.parent_post_id = post_id
                comment.message = request.POST['message']
                comment.save()
                
                url = '/forum/post/%s' %post_id
                return HttpResponseRedirect(url )            
            else:
                base_vars.update({"post":post,"commentform":CommentForm ,"comments":comment_post})
                render_to_response('post.html',base_vars)
        else:        
            base_vars.update({"post":post,"commentform":CommentForm,"comments":comment_post})
            return render_to_response('post.html',base_vars)

    else:
        base_vars.update({"message":"You are not authorised to be here"})
        return render_to_response("message.html",base_vars)


def delete_post(request,post_id):
    delete_post = post_model.objects.get( id = post_id)
    delete_post.delete()
    delete_comments = comment_model.objects.filter( parent_post_id = post_id )
    delete_comments.delete()
    return HttpResponseRedirect('/forum/')

def delete_comment(request,comment_id,post_id):
    delete_comment = comment_model.objects.get( id = comment_id)
    delete_comment.delete()
    
    return HttpResponseRedirect('/forum/post/%s' % post_id)
