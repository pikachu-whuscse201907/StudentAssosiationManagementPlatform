from .Cookie import *
from .check_valid import *
from .verify import *
from .database.delete import *
from .database.save import *
from .database.search import *

def update_user_info(cookie_id, info):
    ''''To be added'''


def get_user_info(cookie_id):
    ''''To be added'''


def userpage(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return response_not_logged_in(request)
    result = get_user_info(cookie_id)
    if not result['success'] :
        return response_not_logged_in(request)
    info = result['info']

    context['islogin'] = True
    context['sex']= info['gender']
    context['motto']= info['motto']
    context['birth_date']= info['birth_date']
    response=HttpResponse(render(request, 'userpage.html',context))
    return response


def updateuserinfo(request):
    context = {}
    cookie_id = request.COOKIES.get('id', None)
    if cookie_id is None:
        return response_not_logged_in(request)
    user = user_of_cookie(cookie_id)
    if user is not None :
        return response_not_logged_in(request)
    context['islogin'] = True

    info={}
    gender = request.POST.get('gender', None)
    motto = request.POST.get('motto', None)
    birth_date = request.POST.get('birth_date', None)

    try:
        info['gender']=int(gender)
        info['birth_date'] = datetime.datetime.strptime(birth_date, '%Y-%m-%d')
        assert motto is not None
        info['motto']=motto
    except:
        fail_notice = 'Illegal data format!'
        context['title'] = fail_notice
        context['url'] = '../updateuserinfo/'
        context['error_msg'] = fail_notice
        return HttpResponse(render(request, 'jump.html', context))

    try:
        result = update_user_info(cookie_id, info)
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

