from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from .database import function
from . import view


def clubactivities(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    context['activities'] = []
    response = HttpResponse(render(request, 'clubactivities.html', context))
    return response
# Ending of function clubactivities(request)


def myactivity(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    
    response = HttpResponse(render(request, 'myactivity.html', context))
    return response
# Ending of function myactivity(request)
