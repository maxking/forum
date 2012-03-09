from django.http import HttpResponseRedirect
from django.contrib.auth.models import AnonymousUser

def get_base_vars(request):
    logged = request.user.is_authenticated()

    # Check for staff access
    if request.user.is_anonymous():
        staff = False
        user = None
    else:
        staff = request.user.is_staff
        user = request.user.email

    result ={'logged':logged,
            'user':user,
            'staff':staff,}

    return result

