from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import datetime
from .Cookie import Cookie
from .database.delete import delete_cookie
from .database.save import save_cookie
from .database.search import user_of_username, user_of_cookie
from .database import function, search
import os
from . import view


def userpage(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    context['sex'] = {
        1: 'MALE',
        2: 'FEMALE'
    }.get(info['gender'], 'UNKNOWN')
    context['motto'] = info['motto']
    context['img'] = info['user_logo']
    
    if info['birth_date'] is None:
        context['birth_date'] = 'Not Specified'
    else:
        context['birth_date'] = info['birth_date'].strftime('%Y-%m-%d')
    
    response = HttpResponse(render(request, 'userpage.html', context))
    return response
# Ending of function userpage(request)


def updateuserinfo(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    context['sex'] = info['gender']
    context['motto'] = info['motto']
    context["img"] = info['user_logo']
    
    if info['birth_date'] is None:
        context['birth_date'] = 'Not Specified'
    else:
        context['birth_date'] = info['birth_date'].strftime('%Y-%m-%d')
    
    gender = request.POST.get('gender', None)
    motto = request.POST.get('motto', None)
    birth_date = request.POST.get('birth_date', None)
    print(type(birth_date))
    print(birth_date)
    
    if gender is None or motto is None or birth_date is None:
        response = HttpResponse(render(request, 'updateuserinfo.html', context))
        return response
    
    info = {}
    
    user_logo = request.FILES.get('user_photo', None)
    if user_logo is not None:
        info['user_logo'] = user_logo
    
    try:
        info['gender'] = int(gender)
        if not 0 <= info['gender'] <= 2:
            info['gender'] = 0
        if 0 < len(birth_date):
            info['birth_date'] = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        info['motto'] = motto
    
    except ValueError:
        fail_notice = 'Update Failed'
        context['title'] = fail_notice
        context['url'] = '../updateuserinfo/'
        context['error_msg'] = fail_notice
        return HttpResponse(render(request, 'jump.html', context))
    
    try:
        result = function.update_user_info(cookie_id, info) # update database
        
        assert result['success'] == True
    
    except AssertionError:
        fail_notice = result['notice'] + '<br/>Jumping back to update page...'
        context['title'] = 'Update Failed'
        context['url'] = '../userpage/'
        context['error_msg'] = fail_notice
        return HttpResponse(render(request, 'jump.html', context))
    
    context['title'] = 'Update Success'
    context['url'] = '../userpage/'
    context['error_msg'] = 'You have updated your information successfully!'
    return HttpResponse(render(request, 'jump.html', context))
# Ending of function updateuserinfo(request)


def myclub(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    user_info = search.user_info_of_username(info['user_name'])
    
    # This class is ONLY for page 'myclub/'
    class __Club:
        def __init__(self, org_logo, organization_name, description,
                     apply_time='', solve_time='', status=''):
            self.org_logo = org_logo
            self.organization_name = organization_name
            self.description = description
            self.apply_time = apply_time
            self.solve_time = solve_time
            self.status = status
    
    # 我管理的社团
    my_managed_clubs = user_info.organization_master.filter(create_status=1)  # status or org.
    managedclubs = []
    for managed_club in my_managed_clubs:
        managedclubs.append(__Club(org_logo=managed_club.org_logo,
                                   organization_name=managed_club.organization_name,
                                   description=managed_club.description))
    context['hasmanagedclub'] = (0 < len(managedclubs))
    context['managedclubs'] = managedclubs

    # 我加入的社团
    my_joined_clubs = user_info.organization_members.all().order_by('organization_name')
    joinedclubs = []
    for joined_club in my_joined_clubs:
        if user_info != joined_club.master:  # if this club wasn't shown above, show here.
            joinedclubs.append(__Club(org_logo=joined_club.org_logo,
                                      organization_name=joined_club.organization_name,
                                      description=joined_club.description))
    context['hasjoinedclub'] = (0 < len(joinedclubs))
    context['joinedclubs'] = joinedclubs
    
    # 我申请加入的社团
    my_applications = user_info.membershipapplication_applicant.all().order_by('-apply_time')
    appliedclubs = []
    for application in my_applications:
        apply_time = None
        solve_time = None
        if application.apply_time is not None:
            apply_time = application.apply_time.strftime('%Y-%m-%d %H:%M:%S')
        if application.solve_time is not None:
            solve_time = application.solve_time.strftime('%Y-%m-%d %H:%M:%S')
        appliedclubs.append(__Club(org_logo=application.organization.org_logo,
                                   organization_name=application.organization.organization_name,
                                   description=application.organization.description,
                                   apply_time=apply_time,
                                   solve_time=solve_time,
                                   status=application.application_status))
    context['hasappliedclub'] = (0 < len(appliedclubs))
    context['appliedclubs'] = appliedclubs
    
    # 我创建的社团
    my_createdclubs = user_info.organization_creator.all().order_by('-create_date')
    createdclubs = []
    for created_club in my_createdclubs:
        apply_time = None
        if created_club.create_date is not None:
            apply_time = created_club.create_date.strftime('%Y-%m-%d %H:%M:%S')
        createdclubs.append(__Club(org_logo=created_club.org_logo,
                                   organization_name=created_club.organization_name,
                                   description=created_club.description,
                                   apply_time=apply_time,
                                   solve_time=None,
                                   status=created_club.create_status))
    context['hascreatedclub'] = (0 < len(createdclubs))
    context['createdclubs'] = createdclubs
    
    response = HttpResponse(render(request, 'myclub.html', context))
    return response
# Ending of function myclub(request)


def mybulletin(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    result = function.get_user_info(cookie_id)
    info = result['info']
    if not result['success']:
        return view.response_not_logged_in(request)
    context['islogin'] = True
    context['name'] = info['user_name']
    context['user_logo'] = info['user_logo']
    
    
    response = HttpResponse(render(request, 'mybulletin.html', context))
    return response
# Ending of function mybulletin(request)
