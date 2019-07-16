from .database import function, search, save
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from . import view,view_special
from people.models import Organizations, ClubAnnouncements
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
        context['title'] = 'Cannot find the club.'
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
    context['announcements'] = []
    for p in org[0].announcements.all():
        context['announcements'].append(Pronounce(p.title, p.create_date.strftime('%Y-%m-%d %H:%M:%S'), p.content))
    
    context['have_announcement'] = (len(context['announcements']) != 0)
    
    return HttpResponse(render(request, 'clubbulletin.html', context))


def addannouncement(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    
    org_name = request.POST.get('org_name', None)
    announcement_title = request.POST.get('announcement_title', None)
    announcement_content = request.POST.get('announcement_content', None)
    org = Organizations.objects.filter(organization_name=org_name)
    if 0 == len(org):
        return HttpResponseRedirect('../index/')
    
    if announcement_content is None or announcement_title is None\
            or 0 == len(announcement_title) or 0 == len(announcement_content):
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
        context['error_msg'] = 'Only club managers can publish announcements!'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
        
    context['islogin'] = True
    context['name'] = info['user_name']
    context['org_name'] = org_name
    new_announcement = ClubAnnouncements.objects.create(title=announcement_title,\
                                                  create_date=datetime.datetime.now(),\
                                                  content=announcement_content)
    org[0].announcements.add(new_announcement)
    org[0].save()

    context['title'] = 'New announcement published.'
    context['url'] = '../clubbulletin/?iden='+org_name
    context['error_msg'] = 'New announcement published.'
    response = HttpResponse(render(request, 'jump.html', context))
    return response


def clubmembers(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    
    org_name = request.GET.get('iden', None)
    org = Organizations.objects.filter(organization_name=org_name)
    if 0 == len(org):
        context['title'] = 'Cannot find the club.'
        context['url'] = '../searchclub/'
        context['error_msg'] = 'Cannot find a club named "org_name".'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    if search.user_info_of_username(info['user_name']) not in org[0].members.all():
        context['title'] = 'Not Authorized.'
        context['url'] = '../clubinfo/?iden=' + org_name
        context['error_msg'] = 'Only club member can see the members.'
        response = HttpResponse(render(request, 'jump.html', context))
        return response
    
    if info['user_name'] == org[0].master.name.name:
        context['ismanager'] = True
    else:
        context['ismanager'] = False
    
    context['islogin'] = True
    context['name'] = info['user_name']
    context['org_name'] = org_name
    context['members'] = []
    for member in org[0].members.all():
        context['members'].append(member)
    
    context['have_member'] = (len(context['members']) != 0)
    
    return HttpResponse(render(request, 'clubmembers.html', context))