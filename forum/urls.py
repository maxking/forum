from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from wiki.views import *
from django.conf import settings
from wiki.forum.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', forum_index),
    (r'^comments$',include('django.contrib.comments.urls')),
    (r'^newpost$', newpost), 
    (r'^post/(?P<post_id>\d+)/$',post_page),
    (r'^post/delete/(?P<post_id>\d+)/$',delete_post),
    (r'^post/(?P<post_id>\d+)/delete/comment/(?P<comment_id>\d+)/$',delete_comment),
                       # Examples:
    # url(r'^$', 'wiki.views.home', name='home'),
    # url(r'^wiki/', include('wiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
                       )+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
