from .Cookie import *
from .verify import *
from .database.delete import delete_cookie
from .database.save import save_cookie
from .database.search import user_of_username, user_of_cookie
from .database import function, search
import os
from . import view


def userpage(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return view.response_not_logged_in(request)
    
    result = function.get_user_info(cookie_id)  # call database
    if not result['success']:
        return view.response_not_logged_in(request)
    info = result['info']
    
    context['islogin'] = True
    context['name'] = info['user_name']
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
    if cookie_id is None:
        return view.response_not_logged_in(request)
    
    result = function.get_user_info(cookie_id)  # call database
    if not result['success']:
        return view.response_not_logged_in(request)
    info = result['info']
    
    context['islogin'] = True
    context['name'] = info['user_name']
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
    user = search.user_of_cookie(cookie_id)
    user_info = search.user_info_of_user(user)
    
    if user_info is None:
        return view.response_not_logged_in(request)
    
    context['islogin'] = True
    context['name'] = user_info.name.name
    
    # This class is ONLY for page 'myclub/'
    class __Club:
        def __init__(self, org_logo, organization_name, description, status=''):
            self.org_logo = org_logo
            self.organization_name = organization_name
            self.description = description
            self.status = status
    
    # 我加入的社团
    my_joined_clubs = user_info.organization_members.all()# status=
    joinedclubs = []
    for joined_club in my_joined_clubs:
        joinedclubs.append(__Club(joined_club.org_logo, joined_club.organization_name,
                                  joined_club.description))
    context['hasjoinedclub'] = (0 < len(joinedclubs))
    context['joinedclubs'] = joinedclubs
    
    # 我管理的社团
    my_managed_clubs = user_info.organization_master.all()# status=
    managedclubs = []
    for managed_club in my_managed_clubs:
        managedclubs.append(__Club(managed_club.org_logo, managed_club.organization_name,
                                   managed_club.description))
    context['hasmanagedclub'] = (0 < len(managedclubs))
    context['managedclubs'] = managedclubs
    
    # 我申请的社团
    my_applications = user_info.membershipapplication_applicant.all()
    appliedclubs = []
    for application in my_applications:
        appliedclubs.append(__Club(application.organization.org_logo,
                                   application.organization.organization_name,
                                   application.organization.description,
                                   application.application_status))
    context['hasappliedclub'] = (0 < len(appliedclubs))
    context['appliedclubs'] = appliedclubs
    
    # 我创建的社团
    my_createdclubs = user_info.organization_creator.all()
    createdclubs = []
    for created_club in my_createdclubs:
        createdclubs.append(__Club(created_club.org_logo, created_club.organization_name,
                                   created_club.description ))# , created_club.status ))
    context['hascreatedclub'] = (0 < len(createdclubs))
    context['createdclubs'] = createdclubs
    
    response = HttpResponse(render(request, 'myclub.html', context))
    return response

# Ending of function myclub(request)
