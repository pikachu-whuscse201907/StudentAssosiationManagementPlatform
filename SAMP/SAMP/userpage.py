from .Cookie import *
from .verify import *
from .database.delete import delete_cookie
from .database.save import save_cookie
from .database.search import user_of_username, user_of_cookie
from .database.function import *
import os
from .settings import MEDIA_URL, MEDIA_ROOT
from PIL import Image


def userpage(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return response_not_logged_in(request)

    result = get_user_info(cookie_id)  # call database
    if not result['success'] :
        return response_not_logged_in(request)
    info = result['info']

    context['islogin'] = True
    context['name']=info['user_name']
    context['sex']= {
                1: 'MALE',
                2: 'FEMALE'
            }.get(info['gender'], 'UNKNOWN')
    context['motto']= info['motto']
    context['img'] = info['user_logo']

    if info['birth_date'] is None:
        context['birth_date'] = 'Not Specified'
    else:
        context['birth_date']= info['birth_date'].strftime('%Y-%m-%d')

    response=HttpResponse(render(request, 'userpage.html',context))
    return response


def updateuserinfo(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return response_not_logged_in(request)

    result = get_user_info(cookie_id)  # call database
    if not result['success']:
        return response_not_logged_in(request)
    info = result['info']

    context['islogin'] = True
    context['name'] = info['user_name']
    context['sex'] = info['gender']
    context['motto'] = info['motto']
    context['img'] = info['user_logo']

    if info['birth_date'] is None:
        context['birth_date'] = 'Not Specified'
    else:
        context['birth_date'] = info['birth_date'].strftime('%Y-%m-%d')

    gender = request.POST.get('gender', None)
    motto = request.POST.get('motto', None)
    birth_date = request.POST.get('birth_date', None)

    if gender is None or motto is None or birth_date is None:
        response = HttpResponse(render(request,'updateuserinfo.html',context))
        return response

    info = {}

    user_logo = request.FILES.get('user_photo', None)
    if user_logo is not None:
        info['user_logo'] = user_logo
        print('user_logo is not None')

    try:
        info['gender']=int(gender)
        info['birth_date'] = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        info['motto']=motto

    except ValueError:
        fail_notice = 'Illegal data format!'
        context['title'] = fail_notice
        context['url'] = '../updateuserinfo/'
        context['error_msg'] = fail_notice
        return HttpResponse(render(request, 'jump.html', context))

    try:
        result = update_user_info(cookie_id, info) # update database

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

