from .Cookie import *
from .check_valid import *
from .verify import *
from .database.delete import *
from .database.save import *
from .database.search import *


def userpage(request):
    user = None
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is not None:
        user = user_of_cookie(cookie_id)
    if user is None:
        return response_not_logged_in(request)
    context = {}
    context['name']=user.name
    # context['year']=
    # context['mon']=
    # context['motto']=
    # context['sex']=
    response=HttpResponse(render(request, 'userpage.html',context))
    return response


def update_user_info(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is not None:
        user = user_of_cookie(cookie_id)
    if user is None:
        return response_not_logged_in(request)