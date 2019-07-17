from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import view, view_special
from people.models import Person, Organizations, ClubAnnouncements, User_info, MembershipApplication
from .database import function, search

def passwd(request):
    content = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return view.response_not_logged_in(request)
    
    result = function.get_user_info(cookie_id)  # call database
    if not result['success']:
        return view.response_not_logged_in(request)
    info = result['info']
    content['name'] = info['user_name']
    return HttpResponse(render(request,'passwd.html',content))

def checkpsd(request):

    return HttpResponse("False")
