from django.conf.urls.defaults import *
from wiki import settings
from wiki.account.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
     (r'^$',index),
     (r'^signupform/?$',signupform),
     (r'^signup/?$',signup),
     (r'^logout/?$',logout),
     (r'^settings/?',settings),
     (r'^home/$',home),
    # Examples:
    # url(r'^$', 'wiki.views.home', name='home'),
    # url(r'^wiki/', include('wiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
