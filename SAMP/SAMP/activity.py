from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime
from .database import function, search
from . import view
from people.models import Person, MembershipApplication, Organizations, Activ


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

    org_name = request.GET.get('iden', None)
    org = Organizations.objects.filter(organization_name=org_name)
    if 0 == len(org):
        context['title'] = 'Cannot find the club.'
        context['url'] = '../searchclub/'
        context['error_msg'] = 'Cannot find a club named "' + org_name + '".'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    # Question: can non-club-member see activities?
    user_info = search.user_info_of_username(info['user_name'])
    '''if user_info not in org[0].members.all():
        context['title'] = 'Not Authorized.'
        context['url'] = '../clubpage/?iden=' + org_name
        context['error_msg'] = 'Only club member can see the activities.'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    '''

    if info['user_name'] == org[0].master.name.name:
        context['ismanager'] = True
    else:
        context['ismanager'] = False

    context['org_name'] = org_name
    context['org_logo'] = org[0].org_logo

    result = function.look_org_activ(cookie_id, org_name)
    if not result['success']:
        context['title'] = 'Access denied.'
        context['url'] = '../clubpage/?iden=' + org_name
        context['error_msg'] = result['notice']
        response = HttpResponse(render(request, 'jump.html', context))
    
    class __Activity:
        def __init__(self, big, org_name, activ_name, activ_place, activ_content, activ_time=''):
            self.big = big  # Boolean
            self.org_name = org_name
            self.activ_name = activ_name
            self.activ_place = activ_place
            self.activ_content = activ_content
            self.activ_time = activ_time

    context['activities'] = []
    activity_list = result['activ_list']
    for each in activity_list:
        context['activities'].append(__Activity(
            big=False,
            org_name=each['org_name'],
            activ_name=each['activ_name'],
            activ_place=each['activ_place'],
            activ_content=each['activ_content'],
            activ_time=each['activ_time'].strftime('%Y-%m-%d %H:%M:%S')
        ))
    context['hasactivities'] = (0 < len(context['activities']))
    if context['hasactivities']:
        context['activities'][0].big =True
    
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
    
    context['activities'] = []
    context['hasactivities'] = (0 < len(context['activities']))
    
    context['joinedactivities'] = []
    context['hasjoinedactivities'] = (0 < len(context['joinedactivities']))
    
    response = HttpResponse(render(request, 'myactivity.html', context))
    return response
# Ending of function myactivity(request)


def addactivity(request):
    context = {}
    
    response = HttpResponse(render(request, 'clubactivities.html', context))
    return response
# Ending of function addactivity(request)
