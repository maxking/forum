from django.conf.urls.defaults import patterns, include, url
from django.conf.urls.static import static
from wiki.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', home),
    (r'^account/',include('wiki.account.urls')),
    (r'^upload/',include('wiki.upload.urls')), 
    (r'^forum/',include('wiki.forum.urls')),                   
                       # Examples:
    # url(r'^$', 'wiki.views.home', name='home'),
    # url(r'^wiki/', include('wiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
