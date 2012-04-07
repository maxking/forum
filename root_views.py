from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser

def get_base_vars(request):
    logged = request.user.is_authenticated()
     
    # Check for staff access
    if request.user.is_anonymous():
        staff = False
        user_email = None
        user_name = None
    else:
        staff = request.user.is_staff
        user_email = request.user.email
        user_name = "%s %s" %(request.user.first_name, request.user.last_name)
        

    result ={'logged':logged,
            'user':user_email,
             'user_name':user_name,
            'staff':staff,}

    return result

