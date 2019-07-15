from .database import function, search, save
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import view,view_special
from people.models import Organizations, ClubPronounces
import datetime


class Pronounce:
    def __init__(self, title, date, content):
        self.title = title
        self.date = date
        self.content = content


def clubbulletin(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    
    org_name = request.GET.get('iden', None)
    org = Organizations.objects.filter(organization_name=org_name)
    if 0 == len(org):
        context['title'] = 'Cannot find specified club.'
        context['url'] = '../searchclub/'
        context['error_msg'] = 'Cannot find a club named "org_name".'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    if search.user_info_of_username(info['user_name']) not in org[0].members.all():
        context['title'] = 'Not Authorized.'
        context['url'] = '../clubinfo/?iden='+org_name
        context['error_msg'] = 'Only club member can see the bulletin.'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    if info['user_name'] == org[0].master.name.name:
        context['ismanager'] = True
    else:
        context['ismanager'] = False
    
    context['islogin'] = True
    context['name'] = info['user_name']
    context['org_name'] = org_name
    context['pronounces'] = []
    for p in org[0].pronounces.all():
        context['pronounces'].append(Pronounce(p.title, p.create_date.strftime('%Y-%m-%d %H:%M:%S'), p.content))
    
    context['have_pronounce'] = (len(context['pronounces']) != 0)
    
    return HttpResponse(render(request, 'clubbulletin.html', context))


def addpronounce(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    
    org_name = request.POST.get('org_name', None)
    pronounce_title = request.POST.get('pronounce_title', None)
    pronounce_content = request.POST.get('pronounce_content', None)
    org = Organizations.objects.filter(organization_name=org_name)
    if 0 == len(org):
        return HttpResponseRedirect('../index/')
    
    if pronounce_content is None or pronounce_title is None\
            or 0 == len(pronounce_title) or 0 == len(pronounce_content):
        context['title'] = 'Illegal Pronounce'
        context['url'] = '../clubbulletin/?iden='+org_name
        context['error_msg'] = '公告标题和公告内容均不可为空'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    if info['user_name'] == org[0].master.name.name:
        context['ismanager'] = True
    else:
        context['ismanager'] = False
        context['title'] = 'Not Authorized.'
        context['url'] = '../clubbulletin/?iden='+org_name
        context['error_msg'] = 'Only club managers can publish pronounces!'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
        
    context['islogin'] = True
    context['name'] = info['user_name']
    context['org_name'] = org_name
    new_pronounce = ClubPronounces.objects.create(title=pronounce_title,\
                                                  create_date=datetime.datetime.now(),\
                                                  content=pronounce_content)
    org[0].pronounces.add(new_pronounce)
    org[0].save()

    context['title'] = 'New pronounce published.'
    context['url'] = '../clubbulletin/?iden='+org_name
    context['error_msg'] = 'New pronounce published.'
    response = HttpResponse(render(request, 'jump.html', context))
    return response

